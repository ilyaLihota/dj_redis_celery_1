from django import forms


class CalculateForm(forms.Form):
    number = forms.CharField()
