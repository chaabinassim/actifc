from django.contrib import admin
from .models import Product,Category,SubCategory,UnitOfMeasurement,TechSpec,Material,Store

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id')
    readonly_fields = ('category_id',)  
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory_id', 'category')  
    readonly_fields = ('subcategory_id',)  
    search_fields = ('name', 'category__name')  
    list_filter = ('category',) 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_id',  'sub_category', 'brand', 'color')
    readonly_fields = ('product_id',)  
    search_fields = ('name', 'product_id', 'category__name', 'sub_category__name')
    list_filter = ('sub_category', 'brand')



admin.site.register(UnitOfMeasurement)
admin.site.register(TechSpec)
admin.site.register(Material)
# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'contact_phone', 'created_at', 'updated_at')
    search_fields = ('name', 'location', 'contact_email', 'contact_phone')
    list_filter = ('created_at', 'updated_at')

