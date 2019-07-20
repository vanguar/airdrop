from .models import ProductInBasket

def getting_basket_info(request): # Функция осуществляет получение информации из корзины
    session_key = request.session.session_key # сСчитываем ключ сессии.
    if not session_key: # Если нет ключа сессии, то создаём его.
        request.session["session_key"] = 123 # При обновлении Джанго возможно возникнет проблемма. Поэтому нужно дописать вот этот код
        request.session.cycle_key()
    
    products_in_basket = ProductInBasket.objects.filter(session_key = session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count() # По этому ключу ищем какие товары есть у нас в корзине и возвращаем эти товары в корзину. Мы можем это отрисовывать в любом темплейте. count() - подсчитывает количество.

    return locals()