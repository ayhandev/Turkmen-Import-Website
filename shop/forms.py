from django import forms
from .models import Order, RATE_CHOICES , Review
from .bulma_mixin import BulmaMixin

class OrderForm(BulmaMixin, forms.Form):
    address = forms.CharField(label='Ваш Адрес')
    phone = forms.CharField(label='Ваша телефон номер для связи с вами!')

    class Meta:
        model = Order
        fields = ('address', 'phone',)




class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class':'textarea'
    }), label='Оставьте отзыв а товаре!')
    rate = forms.ChoiceField(
        choices=RATE_CHOICES, 
        required=True,
        label='Оцените от 1 до 5'
    )
    
    class Meta:
       model = Review
       fields = ('text', 'rate')
