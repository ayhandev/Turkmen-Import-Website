from django.shortcuts import get_object_or_404, redirect, render
from shop.forms import OrderForm, RateForm, OtherForm
from shop.models import CartItem, Order, OrderProduct, Product, Slide, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from .models import Brand

def products_list(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    products = Product.objects.all().order_by('-created_at')
    slides = Slide.objects.all()
    product_id = request.GET.get('product')
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        cart_item = CartItem.objects.filter(product=product, customer=request.user)
        if not cart_item:
            CartItem.objects.create(customer=request.user, product=product, quantity=1)
            return redirect('shop:products_list')
        for item in cart_item:
            item.quantity += 1
            item.save()
    if category:
        products = products.filter(category=category)

    if brand:
        products = products.filter(brand=brand)

    if search:
        products = products.filter(Q(title__icontains=search) |
                               Q(description__icontains=search))
        if not products.exists():
            return redirect('shop:not')



    meta_description = "Лучшие товары в нашем интернет-магазине Turkmen Import. Купите продукты по отличным ценам."
    meta_keywords = "Turkmen Import, интернет-магазин, купить товары, лучшие предложения"

    return render(request, 'products.html', {
        'products': products,
        'slides': slides,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })

@login_required(login_url='users:or')
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    meta_description = "Ваши товары в корзине на сайте Turkmen Import. Проверьте, сколько вы уже добавили."
    meta_keywords = "корзина, интернет-магазин, Turkmen Import"

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })

@login_required(login_url='users:or')
def delete_cart_item(request, pk):
    CartItem.objects.get(pk=pk).delete()
    return redirect('shop:cart')

@login_required(login_url='users:or')
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

@login_required(login_url='users:or')
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

    meta_description = f"{product.title} - {product.description[:160]}."  # Описание до 160 символов

    # Убедитесь, что keywords является списком или пустой строкой
    keywords = getattr(product, 'keywords', [])
    meta_keywords = ", ".join(keywords) if isinstance(keywords, (list, tuple)) else ""

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })

@login_required(login_url='users:or')
def create_order(request):
    # Получаем все товары в корзине для текущего пользователя
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    form = OrderForm(request.POST)
    if not cart_items:
        return render(request, 'error.html')

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=request.user,
            address=form.cleaned_data['address'],
            phone=form.cleaned_data['phone'],
            total_price=total_price
        )

        # Создание связей между заказом и продуктами
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )

        # Удаление товаров из корзины
        cart_items.delete()

        # Формирование тела сообщения
        body = f'Новый заказ от: {request.user.username}\n' \
               f'Адрес: {order.address}\n' \
               f'Телефон: {order.phone}\n' \
               f'Общая сумма: {total_price} $\n' \
               f'Общее количество: {total_quantity}\n\n' \
               f'Состав заказа:\n'

        for item in OrderProduct.objects.filter(order=order):
            body += f'- {item.product.title} x {item.amount} шт. на сумму {item.total} $.\n'

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
                msg['To'] = settings.EMAIL_HOST_USER
                msg['Subject'] = 'Новый заказ!'

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

@login_required(login_url='users:or')
def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {
        'orders': orders_list
    })

@login_required(login_url='users:or')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, customer=request.user, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop:cart')

@login_required(login_url='users:or')
def del_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('shop:cart')

def about(request):
    meta_description = "О нашем интернет-магазине Turkmen Import. Узнайте больше о нас и нашей продукции."
    meta_keywords = "о нас, интернет-магазин, Turkmen Import"

    return render(request, 'about.html', {
        'meta_description': meta_description,
        'meta_keywords': meta_keywords
    })

def zakaz(request):
    form = OtherForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Сохранение данных формы
        other = form.save(commit=False)
        other.user = request.user
        other.save()

        # Отправка информации о заявке на почту
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
                smtp_server.starttls(context=ssl_context)
                smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                msg = MIMEMultipart()
                msg['From'] = settings.EMAIL_HOST_USER
                msg['To'] = settings.EMAIL_HOST_USER
                msg['Subject'] = 'Новая заявка!'

                body = f'Пользователь: {request.user.username}\n' \
                       f'Название товара: {other.name}\n' \
                       f'Бюджет: {other.price}\n' \
                       f'Телефон: {other.number}\n'

                msg.attach(MIMEText(body, 'plain'))

                smtp_server.send_message(msg)

        except Exception as e:
            print(f"Ошибка при отправке email: {e}")

        return redirect('shop:products')

    return render(request, 'zakaz.html', {
        'form': form
    })


def error_page(request):
    return render(request, 'error.html')



def brands(request):
    brands = Brand.objects.order_by('name')  # Сортируем бренды по имени
    context = {'brands': brands}
    return render(request, 'brands_list.html', context)


def NotFound(request):
    return render(request, 'notfound.html')


def custom_page_not_found_view(request, exception=None):
    return render(request, 'error.html', status=404)
