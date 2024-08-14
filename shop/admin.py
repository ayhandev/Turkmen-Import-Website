from django.contrib import admin
from django.http import HttpRequest

from shop.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_new', 'is_discounted')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('price',)
    search_fields = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    ...


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    ...

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'date', 'rate')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None):
        return False