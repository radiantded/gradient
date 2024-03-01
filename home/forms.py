from django import forms


class UploadFileForm(forms.Form):
    file_1 = forms.FileField(label="Отчёт")
    file_2 = forms.FileField(label="Себестоимость")