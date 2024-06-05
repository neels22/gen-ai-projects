from django import forms

class InputForm(forms.Form):
    message = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'ask your question'}))
