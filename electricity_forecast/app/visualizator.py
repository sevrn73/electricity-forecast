from plotly.offline import plot
from plotly.graph_objects import Scattergl, Layout, Figure


def create_nodal_func_plot(exploitation_method_id: str, nodal_plot_data: dict, modes_data: dict):
    """
    ## Функция построения графика динамики параметров стоимости электричества

    Parameters
    ----------
    :param exploitation_method_id: индикатор типа скважины
    :param nodal_plot_data: данные для построения зависимости дебита от управляющего параметра
    :param modes_data: словарь с ключевыми точками намечаемого и текущего режимов

    :return: plot_fig: график

    ----------
    """
    # без np.zeros из-за отсутствия иногда решений узлового анализа
    x_list, y_list = [], []
    for k in nodal_plot_data:
        if k is not None:
            y_list.append(k[0])
            x_list.append(k[2])

    x_list.sort()
    if exploitation_method_id == 0:
        xaxis = 'f, Гц'
        yaxis = 'Q, м3/сут'

    else:
        xaxis = 'Qзак, м3/сут'
        yaxis = 'Q, м3/сут'

    data = []
    data.append(Scattergl(y=y_list, x=x_list, mode='lines',
                          line={'dash': 'solid', 'color': '#AF479D'},
                          name='Зависимости дебита от управляющего параметра'))
    data.append(Scattergl(y=[modes_data['cur_x']], mode='markers',
                          x=[modes_data['cur_y']], name=f'Текущий режим',
                          marker=dict(size=15, color='#b97ebd')))
    data.append(Scattergl(y=[modes_data['int_x']], mode='markers',
                          x=[modes_data['int_y']], name=f'Намечаемый режим',
                          marker=dict(size=15)))
    layout = Layout(
        xaxis={'title': xaxis},
        yaxis={'title': yaxis}, width=800, height=600, legend=dict(orientation="h"),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', )
    figure = Figure(data=data, layout=layout)
    figure.update_xaxes(linewidth=2, linecolor='#A6A8AB', gridcolor='#A6A8AB')
    figure.update_yaxes(linewidth=2, linecolor='#A6A8AB', gridcolor='#A6A8AB')
    plot_fig = plot(figure, auto_open=False, output_type='div')

    return plot_fig