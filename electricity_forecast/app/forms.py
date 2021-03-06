from django import forms
import datetime


class MainForm(forms.Form):
    dt_date_from = forms.DateField(label='Начало исследуемого периода: ', initial=datetime.datetime.now() - datetime.timedelta(days=3))
    dt_date_to = forms.DateField(label='Конец исследуемого периода: ', initial=datetime.datetime.now())

    periods = [1, 2]
    period = forms.ChoiceField(label='Период: ', choices=([(per, per) for per in periods]), initial=1)

    choices_operating_parameter = [
        ('CONSUMER_VOLUME', 'Объем полного планового потребления, МВт*ч'),
        ('SUPPLIER_VOLUME', 'Объем планового производства, МВт*ч'),
        ('CONSUMER_PRICE', 'Индекс равновесных цен на покупку электроэнергии, руб./МВт*ч'),
        ('SUPPLIER_PRICE', 'Индекс равновесных цен на продажу электроэнергии, руб.МВт*ч'),
        ('MAX_PRICE', 'Максимальный индекс равновесной цены, руб.МВт*ч'),
    ]
    operating_parameter = forms.ChoiceField(label='Исследуемый параметр: ', choices=(choices_operating_parameter), initial=choices_operating_parameter[0][0])

    choices_oes = [
        ('1', 'ОЭС Урала'),
        ('2', 'ОЭС Средней Волги'),
        ('3', 'ОЭС Юга'),
        ('4', 'ОЭС Северо-Запада'),
        ('5', 'ОЭС Центра'),
        ('10', 'ОЭС Сибири'),
    ]
    oes = forms.ChoiceField(label='ОЭС: ', choices=(choices_oes), initial=choices_oes[0][0])