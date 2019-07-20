from django.shortcuts import render
from products.models import * # чтобы не перечислять модели, мы все их импортнём


def product(request, product_id): # принимает request и название переменной с id выбранного товара product_id
    product = Product.objects.get(id=product_id) # достаём id товара и выводим в шаблог

    session_key = request.session.session_key # создаём сессию продукта
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)	

    return render(request, 'products/product.html', locals())

