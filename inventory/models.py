from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Assuming default User model
from datetime import date, time




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





class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)

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
    







class SupplyDemand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the supply demand was created.")
    date = models.DateField(default=date.today,  blank=True, null=True,help_text="Date of the supply demand.")
    time = models.TimeField(default=time(0, 0),  blank=True, null=True,help_text="Time of the supply demand.")
    demander = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who created the supply demand.")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="supply_demands", help_text="Project related to this supply demand.")

    class Meta:
        verbose_name = "Supply Demand"
        verbose_name_plural = "Supply Demands"
        ordering = ['-created_at']
        permissions = [
            ("view_own_supplydemand", "Can view own supply demands"),
        ]

    def __str__(self):
        return f"SupplyDemand {self.pk} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class SupplyDemandItem(models.Model):
    supply_demand = models.ForeignKey(SupplyDemand, on_delete=models.CASCADE, related_name="items", help_text="Related supply demand.")
    quantity = models.PositiveIntegerField(help_text="Quantity of the product requested.")
    designation = models.CharField(max_length=255, help_text="Description of the product in case it is not in the product model.")

    class Meta:
        verbose_name = "Supply Demand Item"
        verbose_name_plural = "Supply Demand Items"

    def __str__(self):
        return f"Item: {self.designation} (x{self.quantity})"






class SupplyDemandReview(models.Model):
    supply_demand = models.ForeignKey(SupplyDemand, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField() 
    time = models.TimeField()  

    class Meta:
        verbose_name = "Supply Demand Review"
        verbose_name_plural = "Supply Demand Reviews"
        ordering = ['-created_at']
        unique_together = ('supply_demand', 'store')  # Unique constraint between supply demand and store
        permissions = [
            ("view_own_reviews", "Can view own reviews"),
            ("view_supplydemandreviews_related_to_its_own_demands", "Can view supply demand reviews related to its own demands"),
        ]

    def __str__(self):
        return f"Review for SupplyDemand {self.supply_demand.pk} by {self.reviewer.username}"


class SupplyDemandReviewItem(models.Model):  
    supply_demand_review = models.ForeignKey(SupplyDemandReview, on_delete=models.CASCADE, related_name='review_items')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, help_text="Product for the item. Can be null if product does not exist.")
    available_quantity = models.PositiveIntegerField(help_text="Quantity of the product available in stock.")
   
    class Meta:
        verbose_name = "Supply Demand Review Item"  
        verbose_name_plural = "Supply Demand Review Items" 

    def __str__(self):
        return f"Review Item: {self.product.name} (Available: {self.available_quantity})"





class SupplyOrder(models.Model):
    supply_demand_review = models.OneToOneField(
        'SupplyDemandReview',
        on_delete=models.CASCADE,
        related_name='supply_order',
        help_text="The Supply Demand Review that generated this order."
    )
    ordered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ordered_supply_orders',
        help_text="The user who placed this supply order."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the order was created.")
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending',
        help_text="The status of the supply order."
    )

    date = models.DateField(
        blank=True,
        null=True,
    )
    time = models.TimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Supply Order"
        verbose_name_plural = "Supply Orders"
        ordering = ['-created_at']
        permissions = [
            ("view_own_orders", "Can view own orders"),
            ("view_orders_related_to_its_own_reviews", "can view orders related to its own reviews"),
        ]

    def __str__(self):
        return f"Supply Order {self.id} - {self.status}"



class SupplyOrderItem(models.Model):
    supply_order = models.ForeignKey(
        'SupplyOrder',
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The supply order to which this item belongs."
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="The product for this item. Can be null if the product does not exist."
    )
    available_quantity = models.PositiveIntegerField(help_text="Quantity of the product available in stock.")
    ordered_quantity = models.PositiveIntegerField(help_text="Quantity of the product ordered.", default=0)
    designation = models.CharField(
        max_length=255,
        help_text="Description of the product in case it is not in the product model."
    )

    class Meta:
        verbose_name = "Supply Order Item"
        verbose_name_plural = "Supply Order Items"

    def __str__(self):
        return f"Order Item: {self.designation or self.product.name} (Available: {self.available_quantity}, Ordered: {self.ordered_quantity})"



class Supplier(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True ,help_text="Name of the supplier.")
    registre_de_commerce = models.CharField(max_length=100, verbose_name="Registre de Commerce")
    nis = models.CharField(max_length=50, verbose_name="NIS")  # NIS (Numéro d'Identification Statistique)
    nif = models.CharField(max_length=50, verbose_name="NIF")  # NIF (Numéro d'Identification Fiscale)
    ai = models.CharField(max_length=50, verbose_name="AI")  # AI (Identifiant d'Agrément)
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(max_length=100, verbose_name="Email")
    
    def __str__(self):
        return f"{self.registre_de_commerce} - {self.nis}"

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"




class PurchaseDemand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the purchase demand was created.")
    date = models.DateField(default=date.today,  help_text="Date of the purchase demand.")
    time = models.TimeField(default=time(0, 0),help_text="Time of the purchase demand.")
    demander = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who created the purchase demand.")

    class Meta:
        verbose_name = "Purchase Demand"
        verbose_name_plural = "Purchase Demands"
        ordering = ['-created_at']
        permissions = [
            ("view_own_purchasedemand", "Can view own purchase demands"),
        ]

    def __str__(self):
        return f"PurchaseDemand {self.pk} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class PurchaseDemandItem(models.Model):
    purchase_demand = models.ForeignKey(PurchaseDemand, on_delete=models.CASCADE, related_name="items", help_text="Related purchase demand.")
    quantity = models.PositiveIntegerField(help_text="Quantity of the product requested.")
    designation = models.CharField(max_length=255, help_text="Description of the product in case it is not in the product model.")

    class Meta:
        verbose_name = "Purchase Demand Item"
        verbose_name_plural = "Purchase Demand Items"

    def __str__(self):
        return f"Item: {self.designation} (x{self.quantity})"




# Bon de Commande (Purchase Order) Model
class BonDeCommande(models.Model):
    purchase_demand = models.OneToOneField(PurchaseDemand, on_delete=models.CASCADE, related_name='bon_de_commande')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='bon_de_commandes')
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()  # Date of the purchase order
    time = models.TimeField()  # Time of the purchase order

    @property
    def total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    class Meta:
        verbose_name = "Bon de Commande"
        verbose_name_plural = "Bons de Commande"

    def __str__(self):
        return f"Bon de Commande for {self.purchase_demand} from {self.supplier} on {self.date}"


# Bon de Commande Item (Purchase Order Item) Model
class BonDeCommandeItem(models.Model):
    bon_de_commande = models.ForeignKey(BonDeCommande, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, help_text="Product for the item.")
    ordered_quantity = models.PositiveIntegerField(help_text="Quantity of the product ordered.")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price of the product.")
    
    @property
    def total_price(self):
        return self.ordered_quantity * self.unit_price

    class Meta:
        verbose_name = "Bon de Commande Item"
        verbose_name_plural = "Bon de Commande Items"

    def __str__(self):
        return f"Item for {self.product.name} in Bon de Commande {self.bon_de_commande}"

