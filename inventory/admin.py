from django.contrib import admin
from .models import (Product,Category,SubCategory,UnitOfMeasurement,TechSpec,Material,Store,Project,
 SupplyDemand, SupplyDemandItem, 
 SupplyDemandReview, SupplyDemandReviewItem,
 SupplyOrder, SupplyOrderItem,
 PurchaseDemand, PurchaseDemandItem,Supplier,
 BonDeCommande, BonDeCommandeItem, 
) 
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



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

    

class SupplyDemandItemInline(admin.TabularInline):
    model = SupplyDemandItem
    extra = 1  # Number of empty forms displayed by default
    fields = ['designation', 'quantity']
    verbose_name = "Supply Demand Item"
    verbose_name_plural = "Supply Demand Items"


@admin.register(SupplyDemand)
class SupplyDemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'demander', 'project']
    list_filter = ['created_at', 'project']
    search_fields = ['id', 'demander__username', 'project__name']
    date_hierarchy = 'created_at'
    inlines = [SupplyDemandItemInline]


@admin.register(SupplyDemandItem)
class SupplyDemandItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'designation', 'quantity', 'supply_demand']
    search_fields = ['designation', 'supply_demand__id']
    list_filter = ['supply_demand__project']




class SupplyDemandReviewItemInline(admin.TabularInline):  # Use TabularInline for a compact table layout
    model = SupplyDemandReviewItem
    extra = 1  # Number of empty item forms to display by default
    fields = ('product', 'available_quantity')  # Fields to display
    autocomplete_fields = ['product']  # Enable autocomplete for the product field if it's configured

@admin.register(SupplyDemandReview)
class SupplyDemandReviewAdmin(admin.ModelAdmin):
    list_display = ('supply_demand', 'reviewer', 'store', 'created_at', 'date', 'time')  # Customize display
    search_fields = ('supply_demand__id', 'reviewer__username', 'store__name')  # Add search functionality
    list_filter = ('store', 'created_at', 'date')  # Add filters
    inlines = [SupplyDemandReviewItemInline]  # Attach the inline
    autocomplete_fields = ['supply_demand', 'reviewer', 'store']  # Enable autocomplete if configured


class SupplyOrderItemInline(admin.TabularInline):
    model = SupplyOrderItem
    extra = 1  # Number of empty item forms to display
    fields = ('product', 'available_quantity', 'ordered_quantity', 'designation')  # Fields to display inline
    readonly_fields = ('available_quantity',)  # Make some fields read-only if needed

@admin.register(SupplyOrder)
class SupplyOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supply_demand_review', 'ordered_by', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('supply_demand_review__id', 'ordered_by__username')
    inlines = [SupplyOrderItemInline]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('registre_de_commerce', 'nis', 'nif', 'ai', 'adresse', 'telephone', 'email')
    search_fields = ('registre_de_commerce', 'nis', 'nif', 'ai', 'adresse', 'telephone', 'email')
    list_filter = ('nis', 'nif', 'ai')

admin.site.register(Supplier, SupplierAdmin)



class PurchaseDemandItemInline(admin.TabularInline):
    model = PurchaseDemandItem
    extra = 1  # Number of empty item forms displayed by default
    fields = ['designation', 'quantity']
    verbose_name = "Purchase Demand Item"
    verbose_name_plural = "Purchase Demand Items"

@admin.register(PurchaseDemand)
class PurchaseDemandAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'date', 'time', 'demander']
    list_filter = ['created_at', 'date', 'demander']
    search_fields = ['demander__username']
    inlines = [PurchaseDemandItemInline]


class BonDeCommandeItemInline(admin.TabularInline):
    model = BonDeCommandeItem
    extra = 1  # Number of empty forms to show by default
    fields = ['product', 'ordered_quantity', 'unit_price']  # Fields to display in the inline form
    autocomplete_fields = ['product']  # Autocomplete for the product field

# Admin for BonDeCommande model
class BonDeCommandeAdmin(admin.ModelAdmin):
    list_display = ['purchase_demand', 'supplier', 'date', 'time', 'created_at']
    search_fields = ['purchase_demand__description', 'supplier__name']
    list_filter = ['date', 'supplier']
    inlines = [BonDeCommandeItemInline]  # Allow adding BonDeCommandeItem inline

# Admin for BonDeCommandeItem model
class BonDeCommandeItemAdmin(admin.ModelAdmin):
    list_display = ['bon_de_commande', 'product', 'ordered_quantity', 'unit_price']
    search_fields = ['bon_de_commande__purchase_demand__description', 'product__name']
    list_filter = ['bon_de_commande']

# Register models with their corresponding admin
admin.site.register(BonDeCommande, BonDeCommandeAdmin)
admin.site.register(BonDeCommandeItem, BonDeCommandeItemAdmin)