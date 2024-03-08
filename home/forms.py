from django import forms
from django.forms import NumberInput


class OzonForm(forms.Form):
    file_1 = forms.FileField(label="Отчёт")
    file_2 = forms.FileField(label="Себестоимость")


class YandexForm(forms.Form):
    united = forms.FileField(label="united")
    mp_services = forms.FileField(label="mp_services")
    netting = forms.FileField(label="netting")
    sebes = forms.FileField(label="sebes")
    period = forms.DateField(
        label="period", widget=NumberInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )
