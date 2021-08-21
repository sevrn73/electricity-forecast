from django import forms
import datetime


class MainForm(forms.Form):
    dt_date_from = forms.DateField(label='Начало исследуемого периода: ', initial=datetime.date.today)
    dt_date_to = forms.DateField(label='Конец исследуемого периода: ', initial=datetime.date.today)

    periods = [1, 2]
    period = forms.ChoiceField(label='Период: ', choices=([(per, per) for per in periods]), initial=1)

    choices_operating_parameter = [
        ('', 'Объем полного планового потребления, МВт*ч'),
        ('', 'Объем планового производства, МВт*ч'),
        ('', 'Индекс равновесных цен на покупку электроэнергии, руб./МВт*ч'),
        ('', 'Индекс равновесных цен на продажу электроэнергии, руб.МВт*ч'),
        ('', 'Максимальный индекс равновесной цены, руб.МВт*ч'),
    ]
    operating_parameter = forms.ChoiceField(label='Исследуемый параметр: ', choices=(choices_operating_parameter), initial=choices_operating_parameter[0])

    choices_oes = [
        ('1', 'ОЭС Урала'),
        ('', 'ОЭС Средней Волги'),
        ('', 'ОЭС Юга'),
        ('', 'ОЭС Северо-Запада'),
        ('', 'ОЭС Центра'),
        ('', 'ОЭС Сибири'),
    ]
    oes = forms.ChoiceField(label='ОЭС: ', choices=(choices_oes), initial=choices_oes[0])