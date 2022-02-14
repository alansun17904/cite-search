from django import forms


class QueryCitationForm(forms.Form):
    query = forms.CharField(label='')
    

