from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from shop.bulma_mixin import BulmaMixin
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_('Ваше имя'), max_length=150)
    email = forms.EmailField(label=_('Ваша электронная почта'))
    password1 = forms.CharField(label=_('Придумайте пароль'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Повторите пароль'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Этот адрес электронной почты уже используется.'))
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')

        if len(password1) < 8:
            raise forms.ValidationError(_('Пароль должен быть длиннее 8 символов.'))

        if username.lower() in password1.lower():
            raise forms.ValidationError(_('Пароль не должен содержать имя пользователя.'))

        return password1


class SignInForm(BulmaMixin, AuthenticationForm):
  username = forms.CharField(label='Ваше имя')
  password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

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








