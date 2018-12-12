from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.core.validators import RegexValidator


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    first_name = models.CharField(verbose_name='Имя', help_text='Укажите Ваше имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', help_text='Укажите Вашу фамилию', max_length=50)
    email = models.EmailField(verbose_name='Email', help_text='Укажите Ваш электронный адрес')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{7,15}$',
                                 message="Номер телефона необходимо вводить в формате: '+799999999'. До 15 цифр.")
    phone_number = models.CharField(validators=[phone_regex], verbose_name='Номер телефона',
                                    help_text='Укажите Ваш номер телефона в формате: +79998887766', max_length=17)
    city = models.CharField(verbose_name='Город', max_length=100)
    postal_code = models.CharField(verbose_name='Почтовый индекс', max_length=20)
    address = models.CharField(verbose_name='Адрес',
                               help_text='Укажите Ваш адрес в формате: Улица, Дом, Корпус, Квартира', max_length=250)
    comments = models.TextField(blank=True, null=True, default=None, verbose_name='Комментарии к заказу')
    status = models.ForeignKey(Status, verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создан')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлён')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость заказа')

    class Meta:
        ordering = ('-created',)  # сортировка по дате создазния Заказа
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Заказ №%s: %s" % (self.id, self.status.name)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, verbose_name='Заказ')
    product = models.ForeignKey(Product, blank=True, null=True, default=None, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Колличество')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Итоговая стоимость')
    is_active = models.BooleanField(default=True, verbose_name='Активирован/Деактивирован')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создан')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлён')

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.quantity) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)
