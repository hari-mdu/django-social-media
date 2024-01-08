from django import forms

class usersform(forms.Form):
    email = forms.CharField(max_length=45)
    password = forms.CharField(widget=forms.PasswordInput())