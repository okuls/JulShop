from django.contrib import admin
from .models import *


class SubscriberAdmin(admin.ModelAdmin):
    # list_display = ['name', 'email']   # выводит необходимые поля в админке
    list_display = [field.name for field in Subscriber._meta.fields]  # выводит все поля в админке
    list_filter = ['name', ]  # фильтр в по полю
    search_fields = ['name', 'email']  # поиск по полю
    fields = ['email']  # отображение поля при редактировании

    # exclude = ['email']                # неотображение поля при редактирование

    class Meta:
        model = Subscriber


admin.site.register(Subscriber, SubscriberAdmin)
