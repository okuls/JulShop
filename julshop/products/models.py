from django.db import models
from django.core.urlresolvers import reverse


# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Активировать / Деактивировать')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])


# Модель товара
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    discount = models.IntegerField(default=0, verbose_name="Скидка")
    stock = models.PositiveIntegerField(verbose_name="Наличие")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создан')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.id, self.slug])


# Модель изображений товара
class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, verbose_name="Товар")
    image = models.ImageField(upload_to='products_images/', verbose_name="Изображение товара")
    is_main = models.BooleanField(default=False, verbose_name='Основное изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активировать / Деактивировать')
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Создан')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return "%s" % self.id
