from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart_item/<int:pk>', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart_item/<int:pk>', views.edit_cart_item, name='edit_cart_item'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('cart/create_order/', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_cart'),
    path('about/', views.about, name='about'),
    path('error/', views.error_page, name='error'),
    path('brands/', views.brands, name='brands'),
    path('NotFound/', views.NotFound, name='not'),
    path('other/', views.zakaz, name='zakaz')

]
