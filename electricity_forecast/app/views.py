import requests
from xml.etree import ElementTree
from django.shortcuts import render
from app.forms import MainForm
from app.visualizator import create_nodal_func_plot


def index(request):
    """
    ## Метод представления главной страницы

    """
    main_form = MainForm(request.POST or None)
    dt_date_from = str(main_form['dt_date_from'].value()).replace('-', '')
    dt_date_to = str(main_form['dt_date_to'].value()).replace('-', '')
    period = int(main_form['period'].value())
    operating_parameter = main_form['operating_parameter'].value()

    print(dt_date_from)

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

    print(xmlDict)
    # x_data = []
    # y_data = []
    plot = '' #create_nodal_func_plot()


    return render(request, 'app/index.html', {
        'main_form': main_form,
        'plot': plot
    })
