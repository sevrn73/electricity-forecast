import requests
from xml.etree import ElementTree
import datetime
import pandas as pd
import statsmodels.api as sm
from django.shortcuts import render
from app.forms import MainForm
from app.visualizator import create_nodal_func_plot

def index(request):
    """
    ## Метод представления главной страницы

    """
    main_form = MainForm(request.POST or None)
    dt_date_from = str(main_form['dt_date_from'].value()).replace('-', '').split(' ')[0]
    dt_date_to = str(main_form['dt_date_to'].value()).replace('-', '').split(' ')[0]
    if request.POST:
        datetimeobject = datetime.datetime.strptime(dt_date_from, '%d.%m.%Y')
        dt_date_from = datetimeobject.strftime('%Y%m%d')
        datetimeobject = datetime.datetime.strptime(dt_date_to, '%d.%m.%Y')
        dt_date_to = datetimeobject.strftime('%Y%m%d')

    period = int(main_form['period'].value())
    operating_parameter = main_form['operating_parameter'].value()
    oes = str(main_form['oes'].value())

    str_dpg_code = 'oes'
    r = requests.get(f'https://www.atsenergo.ru/market/stats.xml?date1={dt_date_from}&date2={dt_date_to}&period={period}&type={str_dpg_code}')

    tree = ElementTree.fromstring(r.content)
    xmlDict = {}
    for sitemap in tree:
        children = sitemap.getchildren()
        l = []
        for i in range(1, 8):
            l.append(children[i].text)
        if children[0].text == 'TARGET_DATE':
            xmlDict['COL'] = l
        else:
            try:
                if xmlDict[children[0].text]:
                    xmlDict[children[0].text].append(l)
            except KeyError:
                xmlDict[children[0].text] = [l]

    operating_parameter_index = xmlDict['COL'].index(operating_parameter)
    x_data = [key for key in xmlDict.keys()][1::][::-1]
    y_data = []
    if period == 1:
        for day in [xmlDict[key] for key in x_data]:
            for item in day:
                if item[1] == oes:
                    y_data.append(float(item[operating_parameter_index]))
        x_data = [f'{day} {hour}' for day in x_data for hour in [i for i in range(24)]]
    else:
        for day in [xmlDict[key] for key in x_data]:
            for item in day:
                if item[0] == oes:
                    y_data.append(float(item[operating_parameter_index]))


    for item in MainForm.choices_operating_parameter:
        if item[0] == operating_parameter:
            y_axis = item[1]

    d = {'Date': x_data, 'Value': y_data}
    df = pd.DataFrame(data=d)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y %H') if period == 1 else pd.to_datetime(df['Date'], format='%d.%m.%Y')
    df.set_index('Date', inplace=True)

    date_forecast = dt_date_to
    forecast = pd.to_datetime(f'{date_forecast}', format='%Y%m%d') + datetime.timedelta(days=2)

    arma_mod30 = sm.tsa.ARMA(df, (3, 0)).fit(disp=False) if period == 1 else sm.tsa.ARMA(df, (1, 0)).fit(disp=False)
    predict_sunspots = arma_mod30.predict(df.index[-1], forecast, dynamic=True)
    prediction_x = []
    for time in predict_sunspots.index.tolist():
        datetimeobject = datetime.datetime.strptime(str(time).split(' ')[0], '%Y-%m-%d')
        prediction_x.append(datetimeobject.strftime('%d.%m.%Y'))
    if period == 1:
        prediction_x = [f'{day} {hour}' for day in prediction_x for hour in [i for i in range(24)]]

    plot = create_nodal_func_plot(x_data, y_data, prediction_x, predict_sunspots.values.tolist(), f'Динамика исследуемого параметра - {operating_parameter}', 'Дата', y_axis)

    return render(request, 'app/index.html', {
        'main_form': main_form,
        'plot': plot
    })
