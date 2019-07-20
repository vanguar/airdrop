from django.db import models
from products.models import Product
from django.db.models.signals import post_save # импортирование сигнала
from django.contrib.auth.models import User
from utils.main import disable_for_loaddata




class Status(models.Model): # Заказ
    name = models.CharField(verbose_name='Статус', max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа' 


class Order(models.Model): # Заказ
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    customer_name = models.CharField(verbose_name='Имя клиента', max_length=64, blank=True, null=True, default=None) # Имя, выполневшего заказ
    customer_email = models.EmailField(verbose_name='email клиента', blank=True, null=True, default=None) # мыло заказа
    customer_phone = models.CharField(verbose_name='Телефон клиента', max_length=48, blank=True, null=True, default=None) # поле может быть пустым. Телефон заказа
    customer_address = models.CharField(verbose_name='Адрес доставки', max_length=128, blank=True, null=True, default=None) # адрес заказа
    total_price = models.DecimalField(verbose_name='Общая цена всех товаров', max_digits=10, decimal_places=2, default=0) # Общая стоимость, которая равняется цене * количество всех товаров. decimal_places=2 - означает 2 знака после запятой 
    comments = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None) # текст комментария
    status = models.ForeignKey(Status)  # Поле со статусом, которое ссылается на модель Status
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы' 

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)       


class ProductInOrder(models.Model): # Товар в заказе
    order = models.ForeignKey(Order, blank=True, null=True, default=None) # Ссылка на заказ. (blank=True - поле может быть пустым), (default==None - если Вы добавляете поле в таблицу и в таблице уже есть другие записи, то в это поле автоматически проставляется значение None, т.е НИЧЕГО)
    product = models.ForeignKey(Product, blank=True, null=True, default=None) # Ссылка на товар. 
    nmb = models.IntegerField(verbose_name='Количество товара', default=1) # количество товара в заказе
    price_per_item = models.DecimalField(verbose_name='Цена на день заказа', max_digits=10, decimal_places=2, default=0) # количество товара
    total_price = models.DecimalField(verbose_name='Общая цена товара', max_digits=10, decimal_places=2, default=0) # Общая стоимость, которая равняется цене * количество определённого товара. decimal_places=2 - означает 2 знака после запятой 
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'    


    def save(self, *args, **kwargs):
        price_per_item = self.product.price # текущая цена. Берём из текущей записи product поле price
        self.price_per_item = price_per_item # текущую запись сохраняем в текущее поле
        print (self.nmb)

        self.total_price = int(self.nmb) * price_per_item # пересчитаем общую стоимость на заказе. Нужно определить, какой наш заказ и какие в нём товары!
        
        super(ProductInOrder, self).save(*args, **kwargs)



@disable_for_loaddata
def product_in_order_post_save(sender, instance, created, **kwargs): # обязательные входящие параметры функции. Эту функцию важно не забыть импортировать
    order = instance.order # наш заказ. Обращаемся не через селф, а через инстанс(переводится как сущность). Т.е ордер сохраняется в данной сущности и аналогия того, что эта строчка сохраняется в таблице базы данных. 
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True) # Мы хотим понять, какие ещё есть товары в нашем заказе. Значит мы должны посчитать эти товары. is_active=True так как товар может быть уже не активен.
    
    order_total_price = 0
    for item in all_products_in_order: # определяем общую стоимость товара. Для этого проходим циклом по всем товарам в этом куэрисети и считываем self.total_price и добавляем в order_total_price
        order_total_price += item.total_price # к этому значению добавляется уже существующее значение

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True) # Это должно создавать не новую запись, а обновить существующую

post_save.connect(product_in_order_post_save, sender=ProductInOrder) # первый параметр - название функции, кот должна вызываться на этом сигнале. 2-й параметр - название модели, с которой слушается этот сигнал


class ProductInBasket(models.Model): # Товар в корзине
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None) # ключ сессии, который отвечае за заказ товара в корзине одного посетителя. Обязательно должны присутствовать дефолтные значения.
    order = models.ForeignKey(Order, blank=True, null=True, default=None) # Ссылка на заказ. (blank=True - поле может быть пустым), (default==None - если Вы добавляете поле в таблицу и в таблице уже есть другие записи, то в это поле автоматически проставляется значение None, т.е НИЧЕГО)
    product = models.ForeignKey(Product, blank=True, null=True, default=None) # Ссылка на товар. 
    nmb = models.IntegerField(verbose_name='Количество товара', default=1) # количество товара в заказе
    price_per_item = models.DecimalField(verbose_name='Цена на день заказа', max_digits=10, decimal_places=2, default=0) # количество товара
    total_price = models.DecimalField(verbose_name='Общая цена товара', max_digits=10, decimal_places=2, default=0) # Общая стоимость, которая равняется цене * количество определённого товара. decimal_places=2 - означает 2 знака после запятой 
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price # текущая цена. Берём из текущей записи product поле price
        self.price_per_item = price_per_item # текущую запись сохраняем в текущее поле
        print (self.nmb)

        self.total_price = int(self.nmb) * price_per_item # пересчитаем общую стоимость на заказе. Нужно определить, какой наш заказ и какие в нём товары!
        
        super(ProductInBasket, self).save(*args, **kwargs)    