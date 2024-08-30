from django import forms
from .models import Order, RATE_CHOICES , Review, other
from .bulma_mixin import BulmaMixin

class OrderForm(BulmaMixin, forms.Form):
    address = forms.CharField(
    label='Ваш Адрес',
    widget=forms.TextInput(attrs={'placeholder': 'Г.Ашхабад...'})
)
    phone = forms.CharField(
    label='Ваш телефон номер для связи с вами!',
    widget=forms.TextInput(attrs={'placeholder': '+993'})
)


    class Meta:
        model = Order
        fields = ('address', 'phone',)




class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'textarea'
    }), label='Оставьте отзыв о товаре!')
    rate = forms.ChoiceField(
        choices=RATE_CHOICES,
        required=True,
        label='Оцените от 1 до 5'
    )

    class Meta:
       model = Review
       fields = ('text', 'rate')

class OtherForm(forms.ModelForm):
    name = forms.CharField(
        label='Названия вашего товара',
        widget=forms.TextInput(attrs={'placeholder': 'Redmagic 9 PRO'})
    )
    price = forms.IntegerField(
        label="Ваш бюджет в манатах TMT",
        widget=forms.TextInput(attrs={'placeholder': '14600 TMT'})
    )
    number = forms.CharField(
        label='Ваш телефон номер для связи с вами!',
        widget=forms.TextInput(attrs={'placeholder': '+993'})
    )

    class Meta:
        model = other
        fields = ('name', 'price', 'number')