from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Assuming default User model





class Category(models.Model):
    category_id = models.CharField(max_length=100, unique=True,blank=True, null=True)  # Unique category identifier
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
def generate_category_id(sender, instance, **kwargs):
    if not instance.category_id:  # Only generate category_id if it is not already set
        # Split the name into words
        words = instance.name.split()

        if len(words) == 1:  # Rule 1: Single word
            abbreviation = words[0][:3].upper()
        elif len(words) == 2:  # Rule 2: Two words
            abbreviation = (words[0][0] + words[1][:2]).upper()
        else:  # Rule 3: Three or more words
            abbreviation = ''.join(word[0] for word in words[:3]).upper()

        instance.category_id = abbreviation





class SubCategory(models.Model):
    subcategory_id = models.CharField(max_length=100, unique=True,blank=True, null=True)  # Unique subcategory identifier
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"



@receiver(pre_save, sender=SubCategory)
def generate_category_id(sender, instance, **kwargs):
    if not instance.subcategory_id:  # Only generate category_id if it is not already set
        # Split the name into words
        words = instance.name.split()

        if len(words) == 1:  # Rule 1: Single word
            abbreviation = words[0][:3].upper()
        elif len(words) == 2:  # Rule 2: Two words
            abbreviation = (words[0][0] + words[1][:2]).upper()
        else:  # Rule 3: Three or more words
            abbreviation = ''.join(word[0] for word in words[:3]).upper()

        instance.subcategory_id = abbreviation


class UnitOfMeasurement(models.Model):
    unit_name = models.CharField(max_length=100, unique=True)  # Unit of measurement (e.g., KG, Litre)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)  # Optional abbreviation (e.g., "kg", "ltr")

    def __str__(self):
        return self.unit_name



class TechSpec(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Technical Specification Name")
    symbol = models.CharField(max_length=50, unique=True, verbose_name="Symbol",null=True,blank=True)
    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Material Name")

    def __str__(self):
        return self.name


    
class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True,blank=True, null=True)  # Unique product identifier
    sub_category = models.ForeignKey(SubCategory, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, related_name="products", on_delete=models.CASCADE,blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)  # Brand of the product
    color = models.CharField(max_length=50, blank=True, null=True)  # Color of the product
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, blank=True, null=True, related_name="products", verbose_name="Material")
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)  # Image of the product
    specification_sheet = models.FileField(upload_to="spec_sheets/", blank=True, null=True)  # Specification sheet

    # Technical specifications
    tech_spec_01 =  models.ForeignKey('TechSpec', on_delete=models.SET_NULL, blank=True, null=True, related_name="products_1", verbose_name="Technical Specification 01")
    tech_spec_01_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Technical Specification Value 1", blank=True, null=True) 
    tech_spec_02 =  models.ForeignKey('TechSpec', on_delete=models.SET_NULL, blank=True, null=True, related_name="products_2", verbose_name="Technical Specification 02")
    tech_spec_02_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Technical Specification Value 2", blank=True, null=True) 
    tech_spec_03 =  models.ForeignKey('TechSpec', on_delete=models.SET_NULL, blank=True, null=True, related_name="products_3", verbose_name="Technical Specification 03")
    tech_spec_03_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Technical Specification Value 3", blank=True, null=True)  
    # Stock field
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



@receiver(pre_save, sender=Product)
def generate_product_id(sender, instance, **kwargs):
    if not instance.product_id:
        # Get the category_id and subcategory_id
        category_id = instance.sub_category.category.category_id if instance.sub_category.category else "CAT"
        subcategory_id = instance.sub_category.subcategory_id if instance.sub_category else "SUB"

        # Base product_id pattern
        base_id = f"{category_id}-{subcategory_id}"

        # Find existing products with similar product_id
        existing_ids = Product.objects.filter(product_id__startswith=base_id).values_list('product_id', flat=True)

        # Generate the next available number
        number = 1
        while f"{base_id}-{number}" in existing_ids:
            number += 1

        # Assign the generated product_id to the instance
        instance.product_id = f"{base_id}-{number}"




class Store(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the store.")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Location or address of the store.")
    contact_email = models.EmailField(blank=True, null=True, help_text="Contact email for the store.")
    contact_phone = models.CharField(max_length=15, blank=True, null=True, help_text="Contact phone number for the store.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the store was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the store was last updated.")
    managers = models.ManyToManyField(User, related_name="stores", blank=True, help_text="Users associated with this store.")
    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['name']

    def __str__(self):
        return self.name
    
