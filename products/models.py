from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Наименование товара', max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True) # т.е, если мы хотим убрать товар из админки, то чтобы его не удаляли, а просто деактивировали и ВСЁ!
    
    def __str__(self):
        return "%s" % (self.name) # По умолчанию будет выводиться имя

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров' 

class Product(models.Model): # Заказ
    name = models.CharField(verbose_name='Наименование товара', max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(verbose_name='Цена на день заказа', max_digits=10, decimal_places=2, default=0) # цена на товар
    discount = models.IntegerField(verbose_name='Скидка на товар', default=0) # Скидка на товар. default=0 - означает, что изначально скидка = 0. 
    category = models.ForeignKey(ProductCategory, verbose_name='Категория товара', blank=True, null=True, default=None) # установим тип товара и сошлёмся на модель ProductType(Эту модель опишем выше)
    short_description = models.TextField(verbose_name='Краткое описание товара', blank=True, null=True, default=None) # поле с кратким описанием товара
    description = models.TextField(verbose_name='Описание товара', blank=True, null=True, default=None) # текст комментария
    #additional_ico = models.TextField(verbose_name='Описание ICO', blank=True, null=True, default=None) # текст комментария
    #step_by_step = models.TextField(verbose_name='Описание step_by_step', blank=True, null=True, default=None) # текст комментария
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт
    

    def __str__(self):
        return "%s, %s" % (self.price, self.name) #для ого, чтобы отображались названия товара, а не 1 меняем self.id на self.name. Также, чтобы отображалась цена, пишем self.price и оборачиваем в скобки

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'   


class ProductImage(models.Model): # Заказ
    product = models.ForeignKey(Product, blank=True, null=True, default=None) # ссылка на продукт
    image = models.ImageField(verbose_name='Фото товара', upload_to='products_images/', null=True, default=None) # , null=True, default=None - обязательные значения
    is_main = models.BooleanField(default=False) # по умолчанию, так как главная картинка должна быть одна, а картинок будет несколько, то это поле будет неактивным
    is_active = models.BooleanField(default=True)
    name = models.CharField(verbose_name='Наименование товара', max_length=64, blank=True, null=True, default=None)
    comments = models.TextField(verbose_name='Комментарий', blank=True, null=True, default=None) # текст комментария
    created = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True, auto_now=False) # в поле значения записываются автоматически
    updated = models.DateTimeField(verbose_name='Обновлён', auto_now_add=False, auto_now=True) # значение будет автоматически изменено, когда делается апдейт

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии' 



