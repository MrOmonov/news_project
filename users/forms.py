from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label='Parol')
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label='Parolni takrorlang')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Foydalanuvchi nomi',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Pochta'
        }

    def clean_password2(self):
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if len(password) > 20:
            raise ValidationError('Parolga 20ta belgidan ortiq kirita olamaysiz')
        if password != password2:
            raise ValidationError('Parollar bir biriga mos kelmadi')
        else:
            return password2


class RegisterBaseForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.CharField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']
        labels = {
            'username': 'Foydalanuvchi nomi',
            'first_name': 'Ism',
            'last_name': "Familiya",
            'email': 'E-mail',
            'password1': 'Parol',
            'password2': 'Parolni takrorlang'
        }

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise ValidationError('Parollar bir biriga mos emas')

        return data['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput)
    class Meta:
        model = Profile
        fields = ['profile_photo', 'date_of_birth','address']
