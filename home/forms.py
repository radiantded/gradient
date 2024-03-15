from django import forms
from django.forms import NumberInput


class OzonForm(forms.Form):
    file_1 = forms.FileField(label="Отчёт")
    file_2 = forms.FileField(label="Себестоимость")


class YandexForm(forms.Form):
    united = forms.FileField(label="united")
    mp_services = forms.FileField(label="mp_services")
    united_netting = forms.FileField(label="united_netting")
    sebes = forms.FileField(label="sebes")
    period = forms.DateField(
        label="period", widget=NumberInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )


class WildberriesForm(forms.Form):
    main = forms.FileField(label="main")
    hran = forms.IntegerField(label="hran")
    reklama = forms.IntegerField(label="reklama")
    sebes = forms.FileField(label="sebes")
