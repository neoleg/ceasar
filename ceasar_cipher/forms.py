from django import forms


class InputForm(forms.Form):
    plaintext = forms.CharField(label='', widget=forms.Textarea)
    key_field = forms.IntegerField(min_value=0, max_value=26, label='', localize=True)
