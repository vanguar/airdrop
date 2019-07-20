from django.contrib import admin
from .models import *



class ProductImageInline (admin.TabularInline):
    model = ProductImage # Делаем привязку на основе этой модели, чтобы вкладывать в другие страницы картинки
    extra = 0 # чтобы не отображались дополнительные 3 поля для загрузки картинок


class ProductCategoryAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
   
    
    class Meta:
        model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductImageInline] # связываем модель ProductImage с Product и на странице товара появится загруженные картинки(по умолчанию 3 шт) в админке
    
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)