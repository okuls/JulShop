from django.shortcuts import render
from products.models import *


# Страница товара
def product(request, product_id):
    product = Product.objects.get(id=product_id)

    session_key = request.session.session_key  # инициализация ключа сессии(уникальный идентификатор)
    if not session_key:                        # если ключ не создан
        request.session.cycle_key()            # создаём в ручную

    print(request.session.session_key)         # вывод ключа в консоль

    return render(request, 'products/product.html', locals())
