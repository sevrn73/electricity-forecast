import requests
from xml.etree import ElementTree
from datetime import datetime
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
        datetimeobject = datetime.strptime(dt_date_from, '%d.%m.%Y')
        dt_date_from = datetimeobject.strftime('%Y%m%d')
        datetimeobject = datetime.strptime(dt_date_to, '%d.%m.%Y')
        dt_date_to = datetimeobject.strftime('%Y%m%d')

    period = int(main_form['period'].value())
    operating_parameter = main_form['operating_parameter'].value()
    oes = main_form['oes'].value()

    print(dt_date_from, dt_date_to)

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
                if item[0] == oes:
                    y_data.append(float(item[operating_parameter_index]))
        x_data = [f'{day} - {hour} ч' for day in x_data for hour in [i for i in range(24)]]
    else:
        for day in [xmlDict[key] for key in x_data]:
            for item in day:
                if item[0] == oes:
                    y_data.append(float(item[operating_parameter_index]))


    for item in MainForm.choices_operating_parameter:
        if item[0] == operating_parameter:
            y_axis = item[1]
    plot = create_nodal_func_plot(x_data, y_data, f'Динамика исследуемого параметра - {operating_parameter}', 'Дата', y_axis)

    return render(request, 'app/index.html', {
        'main_form': main_form,
        'plot': plot
    })
