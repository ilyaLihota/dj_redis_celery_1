from django import forms


class CalculateForm(forms.Form):
    value = forms.CharField()
