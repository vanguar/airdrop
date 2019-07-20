from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CheckoutContactForm 

def basket_adding(request): # Отдаёт нужные нам данные, преобразовывая их в формате json
    return_dict = dict() # словарь
    session_key = request.session.session_key # создаём сессию продукта
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")# будем доставать product_id из request.POST
    nmb = data.get("nmb")# будем доставать nmb из request.POST
    is_delete = data.get("is_delete") #
    
    if is_delete == "true":
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:     
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"nmb": nmb }) # Вытаскиваем из базы данных информацию по товару в корзине и только по данному ключу сессии и сохраняем в новую переменную. get_or_create - функция будет искать по первым двум полям, есть ли в базе данных такая запись. Если такая запись будет находится, тогда ничего не будет делать. Если такой записи не будет, тогда функция будет использовать запись defaults={"nmb"=nmb} и дальше смотрите ниже.
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    # Общий код для двух условий
    products_in_basket = ProductInBasket.objects.filter(session_key = session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb # И будем отдавать в ответ и заполнять словарь.

    return_dict["products"] = list() # Полностью передаём заполненый всей информацией о товаре список. Объявляем список
    
    for item in products_in_basket:
        product_dict = dict() # создаём словарь по нашим товарам, в который мы будем вносить данные
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name # Вносим данные в словарь по имени из цикла в наш словарь
        product_dict["price_per_item"] = item.price_per_item # Вносим данные в словарь по цене из цикла в наш словарь
        product_dict["nmb"] = item.nmb # Вносим данные в словарь по количеству из цикла в наш словарь
        return_dict["products"].append(product_dict) # Добавляем наш словарь в список

    return JsonResponse(return_dict)

def checkout (request):
    session_key = request.session.session_key # Берём текущий session_key из request
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True) # is_active=True - означает, что этот товар не удалён. order__isnull=True - означает, что мы исключаем те значения, которые уже в заказе.
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)
    

    form = CheckoutContactForm(request.POST or None) # Форма принимает значение request.POST или ничего
    if request.POST:
        print(request.POST)
        if form.is_valid(): # проверим, проходит ли данная форма валидацию
            print("yes")
            data = request.POST
            name = data.get("name", "1") # Если писать, как ниже, т.е data["phone"], то, если такого поля не будет, то будет возвращаться ошибка. Следовательно, чтобы этого не было пишем data.get("name")
            phone = data["phone"] # Если такого поля не будет, то будет возвращаться ошибка
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name}) # Считываем поле user и идентифицируем пользователя по введёному мобильному телефону, если пользователь уже есть в базе. Если же нет, то система в перспективе предлагает зарегиться,  т.е если get, то ничего не делаем, если же create - то остаётся телефон + записывается значение defaults={"first_name"=name}
            
            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)# Делаем сперва заказ
            for name, value in data.items(): # Функция items() проходит по словарю и при каждой новой итерации извлекает name, value
                if name.startswith("product_in_basket_"): # Функция startswitch проверяет: если name начинается на product_in_basket_, то выполняется код ниже
                    product_in_basket_id = name.split("product_in_basket_")[1] # тогда мы берём это имя, делим по такому значению product_in_basket_ и берём значение с индексом "1". Индекс можно узнать, просто запринтив ниже. Мы увидим список элементов, в котором элемент и индексом "0" будем пустым, а следующий элемент с индекслм "1" тот, что нас интересует.
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)# Считываем сперва элемент по id
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)
                    
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb, 
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)
                    
       
        else:
            print("no")    
    return render(request, 'orders/checkout.html', locals()) 
    