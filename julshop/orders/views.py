from django.shortcuts import render
from django.http import JsonResponse
from . models import ProductInCart

def cart_adding(request):
    return_dict = {}
    session_key = request.session.session_key
    data = request.POST
    product_id = data.get("product_id")
    number = data.get("number")
    print(request.POST)

    new_product = ProductInCart.objects.create(session_key=session_key, product_id=product_id, quantity=number)
    products_total_number = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_number"] = products_total_number
    return JsonResponse(return_dict)
