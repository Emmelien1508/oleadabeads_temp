from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.CharField(label='E-mail')
    firstname = forms.CharField(label='Voornaam')
    lastname = forms.CharField(label='Achternaam')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Wachtwoord')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Bevestig wachtwoord')
    class Meta:
        model = get_user_model()
        fields = ('email', 'firstname', 'lastname', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            # first call the 'real' __init__()
            super(RegisterForm, self).__init__(*args, **kwargs)
            # then do extra stuff:
            self.fields['email'].help_text = ''
            self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': ''})
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': ''})
            self.fields['password2'].widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='E-mail', label_suffix=': ')
    password = forms.CharField(widget=forms.PasswordInput, label="Wachtwoord", label_suffix=': ')