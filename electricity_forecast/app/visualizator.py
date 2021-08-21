from plotly.offline import plot
from plotly.graph_objects import Scattergl, Layout, Figure


def create_nodal_func_plot(x_list: list, y_list: list, name: str, xaxis: str, yaxis: str):
    """
    ## Функция построения графика динамики параметров стоимости электричества

    Parameters
    ----------
    :param x_list: список с данными по x
    :param y_list: список с данными по y
    :param name: анотация к trace
    :param xaxis: подпись оси y
    :param yaxis: подпись оси y

    :return: plot_fig: график

    ----------
    """
    data = []
    data.append(Scattergl(y=y_list, x=x_list, mode='lines',
                          line={'dash': 'solid', 'color': '#AF479D'},
                          name=name))
    layout = Layout(
        xaxis={'title': xaxis},
        yaxis={'title': yaxis}, width=800, height=500, legend=dict(orientation="h"),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', )
    figure = Figure(data=data, layout=layout)
    figure.update_xaxes(linewidth=2, linecolor='#A6A8AB', gridcolor='#A6A8AB')
    figure.update_yaxes(linewidth=2, linecolor='#A6A8AB', gridcolor='#A6A8AB')
    plot_fig = plot(figure, auto_open=False, output_type='div')

    return plot_fig