from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from shop.bulma_mixin import BulmaMixin



class SignUpForm(BulmaMixin, UserCreationForm):
    username = forms.CharField(label='Ваше имя')

    email = forms.CharField(label='Ваша электронная почта')

    password1 = forms.CharField(label='Придумайте пароль')

    password2 = forms.CharField(label='Повторите пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class SignInForm(BulmaMixin, AuthenticationForm):
  username = forms.CharField(label='Ваше имя')
  password = forms.CharField(label='Пароль')

  class Meta:
      model = User
      fields = ['username', 'password']


class EditProfileForm(BulmaMixin, forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Никнейм')
    email = forms.CharField(label='Электронная почта')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ResetPasswordForm(BulmaMixin, PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Старый пароль',
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Новый пароль',
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']








        