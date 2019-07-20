from django.shortcuts import render
from products.models import * # чтобы не перечислять модели, мы все их импортнём




def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True) # product__is_active=True(чтобы отключённые товары не попадали) Выводим только те, которые активны
    products_images_phones = products_images.filter(product__category__id=1) # если мы задаём фильтрацию в связанных моделях в кверисети, то делаем эту связь не через точку, как в темплейте, а через двойное подчёркивание
    products_images_laptops = products_images.filter(product__category__id=2) # то же самое, только через двойное подчёркивание ставим айди 2, те айди ноутбука
    return render(request, 'landing/home.html', locals())