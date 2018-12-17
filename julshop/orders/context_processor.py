from .models import ProductInCart


def getting_cart_info(request):
    session_key = request.session.session_key   # инициализация ключа сессии(уникальный идентификатор)
    if not session_key:                         # если ключ не создан
        request.session.cycle_key()             # создаём в ручную

    products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
    products_total_number = products_in_cart.count()

    return locals()
