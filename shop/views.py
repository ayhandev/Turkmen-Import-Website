from django.shortcuts import get_object_or_404, redirect, render
from shop.forms import OrderForm, RateForm
from shop.models import CartItem, Order, OrderProduct, Product, Slide, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required(login_url='users/sign_in')
def products_list(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    products = Product.objects.all()
    slides = Slide.objects.all()
    product_id = request.GET.get('product')
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        cart_item = CartItem.objects.filter(product=product, customer=request.user)
        if not cart_item:
            CartItem.objects.create(customer=request.user, product=product, quantity=1)
            return redirect('shop:products')
        for item in cart_item:
            item.quantity += 1
            item.save()
    products = products.filter(category=category) if category else products
    products = products.filter(brand=brand) if brand else products
    products = products.filter(Q(title__icontains=search) | 
                               Q(description__icontains=search)) if search else products

    return render(request, 'products.html', {
        'products': products,
        'slides': slides,
    })


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    

    return render(request, 'cart.html', {
        'cart_items':cart_items, 
        'total_quantity': total_quantity,
        'total_price': total_price
    })
    
    
def delete_cart_item(request, pk):
   cart_item = CartItem.objects.get(pk=pk).delete()
   return redirect('shop:cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == "take":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == 'add':
        cart_item.quantity += 1
        cart_item.save()   
    return redirect('shop:cart')



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    form = RateForm(request.POST or None)

    if not request.session.get(f'viewed_{product.pk}', False):
        product.view_count += 1
        product.save()
        request.session[f'viewed_{product.pk}'] = True

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        return redirect('shop:product_detail', pk=product.pk)
        
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from django.conf import settings
from django.shortcuts import render, redirect
from .models import CartItem, Order, OrderProduct
from .forms import OrderForm

def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    form = OrderForm(request.POST)
    if not cart_items:
        return render(request, 'error.html')
    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()

        # Отправка информации о заказе на почту
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
                smtp_server.starttls(context=ssl_context)
                smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                msg = MIMEMultipart()
                msg['From'] = settings.EMAIL_HOST_USER
                msg['To'] =  settings.EMAIL_HOST_USER 
                msg['Subject'] = 'Новый заказ!'

                body = f'Новый заказ от: {request.user.username}\n' \
                       f'Адрес: {order.address}\n' \
                       f'Телефон: {order.phone}\n' \
                       f'Общая сумма: {total_price} $\n' \
                       f'Общее количество: {total_quantity}\n\n' \
                       f'Состав заказа:\n' 
                       
                
                for cart_item in cart_items:
                    body += f'- {cart_item.product.name}: {cart_item.quantity} шт. на сумму {cart_item.total_price()} руб.\n'

                msg.attach(MIMEText(body, 'plain'))

                smtp_server.send_message(msg)
                
        except Exception as e:
            print(f"Ошибка при отправке email: {e}")

        return redirect('shop:cart')

    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'form': form
    })

    
def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {
        'orders': orders_list
    })

@login_required(login_url='users/sign_in')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, customer=request.user, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop:cart')

def del_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('shop:cart')