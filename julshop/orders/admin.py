from django.contrib import admin
from .models import *


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0

# Модель статусов в админке
class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]  # выводит все поля в админке

# Модель заказов в админке
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]  # выводит все поля в админке
    inlines = [ProductInOrderInline]

# Модель товаров в заказе в админке
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]  # выводит все поля в админке


# Модель товаров в заказе в админке
class ProductInCartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInCart._meta.fields]  # выводит все поля в админке


admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(ProductInCart, ProductInCartAdmin)
