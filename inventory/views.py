from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Category, SubCategory, Product,Store,UnitOfMeasurement, TechSpec, Material,Project,SupplyDemand, SupplyDemandItem,SupplyDemandReview, SupplyDemandReviewItem,SupplyOrder,SupplyOrderItem,PurchaseDemand,PurchaseDemandItem,Supplier,BonDeCommande,BonDeCommandeItem
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone



def render_pdf_view(request, *args, **kwargs):
    # Context to pass to the template
    context = {
        'data': 'This is sample data for the PDF.',
        'logo_url': f"{request.scheme}://{request.get_host()}{settings.STATIC_URL}images/logo-actif-construction-2.png",
    }
    
    # Load and render the template
    template_path = 'pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def home(request):
    return render(request, 'home.html')



# CATEGORY VIEWS
class CategoryListView(LoginRequiredMixin,ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    fields = ['name']
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    fields = ['name']
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category-list')


# SUBCATEGORY VIEWS
class SubCategoryListView(LoginRequiredMixin,ListView):
    model = SubCategory
    template_name = 'subcategories/subcategory_list.html'
    context_object_name = 'subcategories'

class SubCategoryCreateView(LoginRequiredMixin,CreateView):
    model = SubCategory
    fields = ['name', 'category', 'description']
    template_name = 'subcategories/subcategory_form.html'
    success_url = reverse_lazy('subcategory-list')

class SubCategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = SubCategory
    fields = ['name', 'category', 'description']
    template_name = 'subcategories/subcategory_form.html'
    success_url = reverse_lazy('subcategory-list')


# PRODUCT VIEWS
class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    fields = ['name', 'sub_category', 'description','unit_of_measurement','brand', 'color', 'image', 'material', 'tech_spec_01', 'tech_spec_02', 'tech_spec_03', 'tech_spec_01_value','tech_spec_02_value','tech_spec_03_value']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    fields = ['name', 'sub_category', 'description','unit_of_measurement','brand', 'color', 'image', 'material', 'tech_spec_01', 'tech_spec_02', 'tech_spec_03', 'tech_spec_01_value','tech_spec_02_value','tech_spec_03_value']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')



class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    template_name = "stores/store_list.html"
    context_object_name = "stores"



class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    template_name = "stores/store_form.html"
    fields = ['name', 'location', 'contact_email', 'contact_phone', 'managers']
    success_url = reverse_lazy('store_list')

    def form_valid(self, form):
        # Loop through managers and check permissions
        managers = form.cleaned_data.get('managers', [])
        for manager in managers:
            if not manager.has_perm('inventory.add_supplydemandreview'):
                # Add a non-field error to the form if the manager lacks permission
                form.add_error(None, f"{manager.username} does not have the required permission.")
                # Return the form with the error
                return self.render_to_response(self.get_context_data(form=form))

        # Proceed with the normal form processing if no errors
        return super().form_valid(form)
   

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    template_name = "stores/store_form.html"
    fields = ['name', 'location', 'contact_email', 'contact_phone', 'managers']
    success_url = reverse_lazy('store_list')

    def form_valid(self, form):
        # Loop through managers and check permissions
        managers = form.cleaned_data.get('managers', [])
        for manager in managers:
            if not manager.has_perm('inventory.add_supplydemandreview'):
                # Add a non-field error to the form if the manager lacks permission
                form.add_error(None, f"{manager.username} does not have the required permission.")
                # Return the form with the error
                return self.render_to_response(self.get_context_data(form=form))

        # Proceed with the normal form processing if no errors
        return super().form_valid(form)
    
    


# UnitOfMeasurement Views
class UnitOfMeasurementListView(ListView):
    model = UnitOfMeasurement
    template_name = 'units/unit_of_measurement_list.html'
    context_object_name = 'units'

class UnitOfMeasurementCreateView(CreateView):
    model = UnitOfMeasurement
    fields = ['unit_name', 'abbreviation']
    template_name = 'units/unit_of_measurement_form.html'
    success_url = reverse_lazy('unit-of-measurement-list')

class UnitOfMeasurementUpdateView(UpdateView):
    model = UnitOfMeasurement
    fields = ['unit_name', 'abbreviation']
    template_name = 'units/unit_of_measurement_form.html'
    success_url = reverse_lazy('unit-of-measurement-list')


# TechSpec Views
class TechSpecListView(ListView):
    model = TechSpec
    template_name = 'tech/tech_spec_list.html'
    context_object_name = 'tech_specs'

class TechSpecCreateView(CreateView):
    model = TechSpec
    fields = ['name', 'symbol']  # Include the new 'symbol' field
    template_name = 'tech/tech_spec_form.html'
    success_url = reverse_lazy('tech-spec-list')

class TechSpecUpdateView(UpdateView):
    model = TechSpec
    fields = ['name', 'symbol']  # Include the new 'symbol' field
    template_name = 'tech/tech_spec_form.html'
    success_url = reverse_lazy('tech-spec-list')


# Material Views
class MaterialListView(ListView):
    model = Material
    template_name = 'material/material_list.html'
    context_object_name = 'materials'

class MaterialCreateView(CreateView):
    model = Material
    fields = ['name']
    template_name = 'material/material_form.html'
    success_url = reverse_lazy('material-list')

class MaterialUpdateView(UpdateView):
    model = Material
    fields = ['name']
    template_name = 'material/material_form.html'
    success_url = reverse_lazy('material-list')


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name']
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name']
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project-list')




@permission_required("inventory.add_supplydemand", raise_exception=True)
def create_supply_demand(request):
    errors = []  # Context variable to hold validation errors

    # Fetch all available projects
    projects = Project.objects.all()

    if request.method == "POST":
        designations = request.POST.getlist("designations[]")
        quantities = request.POST.getlist("quantities[]")
        project_id = request.POST.get("project")  # Get the selected project ID
        date = request.POST.get("date")  # Get the date input
        time = request.POST.get("time")  # Get the time input

        # Validate project selection
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            errors.append("Selected project does not exist.")
            return render(request, "supply/demand/supply_demand_form.html", {"errors": errors, "projects": projects})

        # Validate date and time
        if not date:
            errors.append("Date is required.")
        if not time:
            errors.append("Time is required.")

        # Ensure the form is not empty
        if not designations or not quantities or len(designations) != len(quantities):
            errors.append("Please add at least one valid item with both designation and quantity.")

        cleaned_data = []  # Collect validated data
        for i, (designation, quantity) in enumerate(zip(designations, quantities)):
            # Validate designation
            if not designation.strip():
                errors.append(f"Item {i + 1}: Designation cannot be empty.")

            # Validate quantity
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    errors.append(f"Item {i + 1}: Quantity must be a positive integer.")
            except ValueError:
                errors.append(f"Item {i + 1}: Quantity must be a valid integer.")

            # If no errors for the current item, add to cleaned data
            if not errors:
                cleaned_data.append({"designation": designation.strip(), "quantity": quantity})

        # If there are validation errors, display them
        if errors:
            return render(request, "supply/demand/supply_demand_form.html", {"errors": errors, "projects": projects})

        # Save the SupplyDemand and items with error handling
        try:
            with transaction.atomic():  # Ensure atomicity for all database operations
                supply_demand = SupplyDemand.objects.create(
                    demander=request.user,
                    project=project,
                    date=date,
                    time=time
                )
                for item in cleaned_data:
                    SupplyDemandItem.objects.create(
                        supply_demand=supply_demand,
                        designation=item["designation"],
                        quantity=item["quantity"],
                    )
        except Exception as e:
            # Log the error to the console and add a generic error message
            print(f"Error saving supply demand: {e}")
            errors.append("An unexpected error occurred while saving the supply demand. Please try again.")
            return render(request, "supply/demand/supply_demand_form.html", {"errors": errors, "projects": projects})

        # Success message and redirect
        messages.success(request, "Supply demand created successfully.")
        return redirect("supply-demand-list")

    return render(request, "supply/demand/supply_demand_form.html", {"errors": [], "projects": projects})


def supply_demand_list(request):
    # Check user permissions and fetch supply demands accordingly
    if request.user.has_perm("inventory.view_supplydemand"):
        # Fetch all SupplyDemand objects
        supply_demands = SupplyDemand.objects.all().order_by('-created_at')
    elif request.user.has_perm("inventory.view_own_supplydemand"):
        # Filter SupplyDemand objects by the current user
        supply_demands = SupplyDemand.objects.filter(demander=request.user).order_by('-created_at')
    else:
        # Raise a 403 error if the user has neither permission
        raise PermissionDenied("You do not have permission to view this page.")

    # Render the supply demand list template
    return render(request, 'supply/demand/supply_demand_list.html', {'supply_demands': supply_demands})


def supply_demand_detail(request, pk):
    # Fetch the SupplyDemand object
    supply_demand = get_object_or_404(SupplyDemand, pk=pk)

    # Check for the first permission
    if request.user.has_perm("inventory.view_supplydemand"):
        # User has permission to view all supply demands
        pass
    elif request.user.has_perm("inventory.view_own_supplydemand"):
        # User has permission to view their own supply demands
        if request.user != supply_demand.demander:
            raise PermissionDenied("You do not have permission to view this supply demand.")
    else:
        # If neither permission is granted, deny access
        raise PermissionDenied("You do not have permission to view this supply demand.")

    # Render the supply demand details in the template
    return render(request, 'supply/demand/supply_demand_detail.html', {'supply_demand': supply_demand})




@permission_required("inventory.add_supplydemandreview", raise_exception=True)
def create_supply_demand_review(request, supply_demand_id):
    errors = []  # Context variable to hold validation errors

    # Fetch all available stores and products
    stores = Store.objects.all()
    products = Product.objects.all()

    if request.method == "POST":
        product_ids = request.POST.getlist("product_ids[]")  # Get the list of product IDs
        available_quantities = request.POST.getlist("available_quantities[]")  # Get the available quantities
        store_id = request.POST.get("store")  # Get the store ID
        date = request.POST.get("date")  # Get the date input
        time = request.POST.get("time")  # Get the time input

        # Validate SupplyDemand object
        try:
            supply_demand = SupplyDemand.objects.get(id=supply_demand_id)
        except SupplyDemand.DoesNotExist:
            errors.append("Selected SupplyDemand does not exist.")
            return render(request, "supply/review/supply_demand_review_form.html", {"errors": errors, "stores": stores, "products": products})

        # Validate store selection
        if not store_id or store_id == "":
            errors.append("Store is required.")
        else:
            try:
                store = Store.objects.get(id=store_id)
            except Store.DoesNotExist:
                errors.append("Store does not exist.")

        # Validate date and time
        if not date:
            errors.append("Date is required.")
        if not time:
            errors.append("Time is required.")

        # Ensure the form is not empty and validate product and quantity data
        if not product_ids or not available_quantities or len(product_ids) != len(available_quantities):
            errors.append("Please add at least one valid item with both product and available quantity.")

        cleaned_data = []  # Collect validated data
        for i, (product_id, available_quantity) in enumerate(zip(product_ids, available_quantities)):
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                errors.append(f"Product with ID {product_id} does not exist.")
                continue  # Skip this iteration if the product doesn't exist

            try:
                available_quantity = int(available_quantity)
                if available_quantity < 0:
                    errors.append(f"Item {i + 1}: Available quantity cannot be negative.")
                else:
                    cleaned_data.append({"product": product, "available_quantity": available_quantity})
            except ValueError:
                errors.append(f"Item {i + 1}: Available quantity must be a valid integer.")

        # If there are validation errors, display them
        if errors:
            return render(request, "supply/review/supply_demand_review_form.html", {
                "errors": errors,
                "stores": stores,
                "products": products,
                "product_ids": product_ids,
                "available_quantities": available_quantities,
                "date": date,
                "time": time
            })

        # Save the SupplyDemandReview and items with error handling
        try:
            with transaction.atomic():  # Ensure atomicity for all database operations
                supply_demand_review = SupplyDemandReview.objects.create(
                    supply_demand=supply_demand,
                    reviewer=request.user,
                    store=store,
                    date=date,
                    time=time
                )
                for item in cleaned_data:
                    SupplyDemandReviewItem.objects.create(
                        supply_demand_review=supply_demand_review,
                        product=item["product"],
                        available_quantity=item["available_quantity"]
                    )
        except Exception as e:
            print(f"Error saving supply demand review: {e}")
            errors.append("An unexpected error occurred while saving the supply demand review. Please try again.")
            return render(request, "supply/review/supply_demand_review_form.html", {
                "errors": errors,
                "stores": stores,
                "products": products,
                "product_ids": product_ids,
                "available_quantities": available_quantities,
                "date": date,
                "time": time
            })

        # Success message and render the confirmation page (or redirect as appropriate)
        messages.success(request, "Supply demand review created successfully.")
        return redirect("supply-demand-review-list")

    # Initial render of the form when GET is requested
    return render(request, "supply/review/supply_demand_review_form.html", {
        "errors": [],
        "stores": stores,
        "products": products
    })


def supply_demand_review_list(request):
    # Check if the user has the `inventory.view_supplydemandreview` permission
    if request.user.has_perm("inventory.view_supplydemandreview"):
        # Fetch all reviews
        supply_demand_reviews = SupplyDemandReview.objects.all()
    elif request.user.has_perm("inventory.view_own_reviews"):
        # Filter reviews by reviewer = request.user
        supply_demand_reviews = SupplyDemandReview.objects.filter(reviewer=request.user)
    elif request.user.has_perm("inventory.view_supplydemandreviews_related_to_its_own_demands"):
        # Filter reviews by supply demands related to the user
        supply_demand_reviews = SupplyDemandReview.objects.filter(
            supply_demand__demander=request.user
        )
    else:
        # Raise a 403 error if the user has neither permission
        raise PermissionDenied("You do not have permission to view this page.")

    # Render the reviews in the template
    return render(request, "supply/review/supply_demand_review_list.html", {"reviews": supply_demand_reviews})


def supply_demand_review_detail(request, pk):
    review = get_object_or_404(SupplyDemandReview, pk=pk)
    return render(request, 'supply/review/supply_demand_review_detail.html', {'review': review})




@permission_required("inventory.add_supplyorder", raise_exception=True)
def create_supply_order(request, supply_demand_review_id):
    errors = []  # Initialize errors list

    # Fetch the SupplyDemandReview based on the passed ID
    supply_demand_review = get_object_or_404(SupplyDemandReview, id=supply_demand_review_id)

    # Fetch related SupplyDemandItemReviews for the review
    supply_demand_item_reviews = supply_demand_review.review_items.all()

    if request.method == "POST":
        # Dictionary to hold ordered quantities
        ordered_quantities = {}

        # Loop through the items in the supply demand review
        for item in supply_demand_item_reviews:
            ordered_quantity = request.POST.get(f'ordered_quantity_{item.id}', 0)

            # Ensure the ordered quantity is a valid number
            try:
                ordered_quantity = int(ordered_quantity)
            except ValueError:
                errors.append(f"Invalid quantity for item {item.product.name}.")
            
            # Check if the ordered quantity is valid
            if ordered_quantity < 0:
                errors.append("Ordered quantity cannot be negative.")
            if ordered_quantity > item.available_quantity:
                errors.append(f"Ordered quantity for {item.product.name} cannot be greater than available quantity.")

            if ordered_quantity >= 0 and ordered_quantity <= item.available_quantity:
                ordered_quantities[item.id] = ordered_quantity

        # Validate date and time fields
        order_date = request.POST.get("order_date", None)
        order_time = request.POST.get("order_time", None)

        if not order_date:
            errors.append("Date is required.")
        if not order_time:
            errors.append("Time is required.")

        # If there are validation errors, return with errors
        if errors:
            return render(request, 'supply/order/create_supply_order.html', {
                'supply_demand_review': supply_demand_review,
                'supply_demand_item_reviews': supply_demand_item_reviews,
                'errors': errors,
            })

        # Attempt to create the SupplyOrder and related items in one atomic transaction
        try:
            with transaction.atomic():
                supply_order = SupplyOrder.objects.create(
                    supply_demand_review=supply_demand_review,
                    ordered_by=request.user,
                    date=order_date,
                    time=order_time,
                )

                # Create SupplyOrderItems for each item in the review
                for item in supply_demand_item_reviews:
                    ordered_quantity = ordered_quantities.get(item.id, 0)
                    if ordered_quantity > 0:
                        SupplyOrderItem.objects.create(
                            supply_order=supply_order,
                            product=item.product,
                            ordered_quantity=ordered_quantity,
                            available_quantity=item.available_quantity,
                        )

            # Success message
            messages.success(request, "Supply order created successfully!")
            return redirect('supply_order_list')

        except Exception as e:
            print(f"Error saving supply order or items: {e}")
            errors.append("An unexpected error occurred while saving the supply order. Please try again.")
            return render(request, 'supply/order/create_supply_order.html', {
                'supply_demand_review': supply_demand_review,
                'supply_demand_item_reviews': supply_demand_item_reviews,
                'errors': errors,
            })

    # Initial render of the form when GET is requested
    return render(request, 'supply/order/create_supply_order.html', {
        'supply_demand_review': supply_demand_review,
        'supply_demand_item_reviews': supply_demand_item_reviews,
        'errors': errors,
    })



def supply_order_list(request):
    # Check if the user has the `inventory.view_supply_orders` permission
    if request.user.has_perm("inventory.view_own_orders"):
        # Filter orders by user who created the order
        supply_orders = SupplyOrder.objects.filter(ordered_by=request.user)
    elif request.user.has_perm("inventory.view_orders_related_to_its_own_reviews"):
        # Filter orders related to the supply demands of the user
        supply_orders = SupplyOrder.objects.filter(
            supply_demand_review__reviewer=request.user
        )
    else:
        # Raise a 403 error if the user has neither permission
        raise PermissionDenied("You do not have permission to view this page.")
    
    # Pass the filtered objects to the template
    return render(request, 'supply/order/supply_order_list.html', {
        'supply_orders': supply_orders,
    })



def supply_order_detail(request, supply_order_id):
    """
    View to display the details of a specific supply order with permission checks.
    """
    # Fetch the supply order object
    supply_order = get_object_or_404(SupplyOrder, id=supply_order_id)

    # Permission: User can view their own orders
    if request.user.has_perm("inventory.view_own_orders"):
        if request.user != supply_order.ordered_by:
            raise PermissionDenied("You do not have permission to view this supply order.")

    # Permission: User can view orders related to their own demands
    elif request.user.has_perm("inventory.view_orders_related_to_its_own_reviews"):
        if request.user != supply_order.supply_demand_review.reviewer:
            raise PermissionDenied("You do not have permission to view this supply order.")

    else:
        # If no relevant permission is granted, deny access
        raise PermissionDenied("You do not have permission to view this supply order.")

    # Fetch related items for the supply order

    # Render the supply order details in the template
    return render(request, 'supply/order/supply_order_detail.html', {
        'supply_order': supply_order,

    })



@permission_required("inventory.add_purchasedemand", raise_exception=True)
def create_purchase_demand(request):
    errors = []  # Context variable to hold validation errors

    if request.method == "POST":
        designations = request.POST.getlist("designations[]")
        quantities = request.POST.getlist("quantities[]")
        date = request.POST.get("date")  # Get the date input
        time = request.POST.get("time")  # Get the time input

        # Validate date and time
        if not date:
            errors.append("Date is required.")
        if not time:
            errors.append("Time is required.")

        # Ensure the form is not empty
        if not designations or not quantities or len(designations) != len(quantities):
            errors.append("Please add at least one valid item with both designation and quantity.")

        cleaned_data = []  # Collect validated data
        for i, (designation, quantity) in enumerate(zip(designations, quantities)):
            # Validate designation
            if not designation.strip():
                errors.append(f"Item {i + 1}: Designation cannot be empty.")

            # Validate quantity
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    errors.append(f"Item {i + 1}: Quantity must be a positive integer.")
            except ValueError:
                errors.append(f"Item {i + 1}: Quantity must be a valid integer.")

            # If no errors for the current item, add to cleaned data
            if not errors:
                cleaned_data.append({"designation": designation.strip(), "quantity": quantity})

        # If there are validation errors, display them
        if errors:
            return render(request, "purchase/demand/purchase_demand_form.html", {"errors": errors})

        # Save the PurchaseDemand and items with error handling
        try:
            with transaction.atomic():  # Ensure atomicity for all database operations
                purchase_demand = PurchaseDemand.objects.create(
                    demander=request.user,
                    date=date,
                    time=time
                )
                for item in cleaned_data:
                    PurchaseDemandItem.objects.create(
                        purchase_demand=purchase_demand,
                        designation=item["designation"],
                        quantity=item["quantity"],
                    )
        except Exception as e:
            # Log the error to the console and add a generic error message
            print(f"Error saving purchase demand: {e}")
            errors.append("An unexpected error occurred while saving the purchase demand. Please try again.")
            return render(request, "purchase/demand/purchase_demand_form.html", {"errors": errors})

        # Success message and redirect
        messages.success(request, "Purchase demand created successfully.")
        return redirect("purchase-demand-list")

    return render(request, "purchase/demand/purchase_demand_form.html", {"errors": []})


def purchase_demand_list(request):
    # Check user permissions and fetch purchase demands accordingly
    if request.user.has_perm("inventory.view_purchasedemand"):
        # Fetch all PurchaseDemand objects
        purchase_demands = PurchaseDemand.objects.all().order_by('-created_at')
    elif request.user.has_perm("inventory.view_own_purchasedemand"):
        # Filter PurchaseDemand objects by the current user
        purchase_demands = PurchaseDemand.objects.filter(demander=request.user).order_by('-created_at')
    else:
        # Raise a 403 error if the user has neither permission
        raise PermissionDenied("You do not have permission to view this page.")

    # Render the purchase demand list template
    return render(request, 'purchase/demand/purchase_demand_list.html', {'purchase_demands': purchase_demands})


def purchase_demand_detail(request, pk):
    # Fetch the PurchaseDemand object
    purchase_demand = get_object_or_404(PurchaseDemand, pk=pk)

    # Check for permissions
    if request.user.has_perm("inventory.view_purchasedemand"):
        # User has permission to view all purchase demands
        pass
    elif request.user.has_perm("inventory.view_own_purchasedemand"):
        # User has permission to view their own purchase demands
        if request.user != purchase_demand.demander:
            raise PermissionDenied("You do not have permission to view this purchase demand.")
    else:
        # If neither permission is granted, deny access
        raise PermissionDenied("You do not have permission to view this purchase demand.")

    # Render the purchase demand details in the template
    return render(request, 'purchase/demand/purchase_demand_detail.html', {'purchase_demand': purchase_demand})


def purchase_demand_pdf(request, pk, *args, **kwargs):
    # Fetch the PurchaseDemand object using the primary key (pk)
    purchase_demand = get_object_or_404(PurchaseDemand, pk=pk)
    
    # Context to pass to the template
    context = {
        'purchase_demand': purchase_demand,  # Pass the actual purchase demand object
        'logo_url': f"{request.scheme}://{request.get_host()}{settings.STATIC_URL}assets/img/logos/logo-actif.jpg",
    }
    
    # Load and render the template
    template_path = 'purchase/demand/purchase_demand_pdf.html'
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="purchase_demand_{purchase_demand.id}.pdf"'  # Set the filename
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # If errors occur during PDF creation, return an error message
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')
    
    # Return the generated PDF
    return response




@permission_required("inventory.add_bondecommande", raise_exception=True)
def create_bon_de_commande(request, purchase_demand_id):
    errors = []  # Context variable to hold validation errors

    # Fetch all available suppliers and products
    suppliers = Supplier.objects.all()
    products = Product.objects.all()


    if request.method == "POST":
        product_ids = request.POST.getlist("product_ids[]")  # Get the list of product IDs
        ordered_quantities = request.POST.getlist("ordered_quantities[]")  # Get the ordered quantities
        unit_prices = request.POST.getlist("unit_prices[]")  # Get the unit prices
        supplier_id = request.POST.get("supplier")  # Get the supplier ID
        date = request.POST.get("date")  # Get the date input
        time = request.POST.get("time")  # Get the time input

        # Validate PurchaseDemand object
        try:
            purchase_demand = PurchaseDemand.objects.get(id=purchase_demand_id)
        except PurchaseDemand.DoesNotExist:
            errors.append("Selected PurchaseDemand does not exist.")
            return render(request, "purchase/command/bon_de_commande_form.html", {"errors": errors, "suppliers": suppliers, "products": products})

        # Validate supplier selection
        if not supplier_id or supplier_id == "":
            errors.append("Supplier is required.")
        else:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
            except Supplier.DoesNotExist:
                errors.append("Supplier does not exist.")

        # Validate date and time
        if not date:
            errors.append("Date is required.")
        if not time:
            errors.append("Time is required.")

        # Ensure the form is not empty and validate product, quantity, and unit price data
        if not product_ids or not ordered_quantities or len(product_ids) != len(ordered_quantities) or len(product_ids) != len(unit_prices):
            errors.append("Please add at least one valid item with product, ordered quantity, and unit price.")

        cleaned_data = []  # Collect validated data
        for i, (product_id, ordered_quantity, unit_price) in enumerate(zip(product_ids, ordered_quantities, unit_prices)):
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                errors.append(f"Product with ID {product_id} does not exist.")
                continue  # Skip this iteration if the product doesn't exist

            try:
                ordered_quantity = int(ordered_quantity)
                unit_price = float(unit_price)
                if ordered_quantity < 0:
                    errors.append(f"Item {i + 1}: Ordered quantity cannot be negative.")
                if unit_price < 0:
                    errors.append(f"Item {i + 1}: Unit price cannot be negative.")
                else:
                    cleaned_data.append({"product": product, "ordered_quantity": ordered_quantity, "unit_price": unit_price})
            except ValueError:
                errors.append(f"Item {i + 1}: Ordered quantity and unit price must be valid numbers.")

        # If there are validation errors, display them
        if errors:
            return render(request, "purchase/command/bon_de_commande_form.html", {
                "errors": errors,
                "suppliers": suppliers,
                "products": products,
                "product_ids": product_ids,
                "ordered_quantities": ordered_quantities,
                "unit_prices": unit_prices,
                "date": date,
                "time": time
            })

        # Save the BonDeCommande and items with error handling
        try:
            with transaction.atomic():  # Ensure atomicity for all database operations
                bon_de_commande = BonDeCommande.objects.create(
                    purchase_demand=purchase_demand,
                    supplier=supplier,
                    date=date,
                    time=time
                )
                for item in cleaned_data:
                    BonDeCommandeItem.objects.create(
                        bon_de_commande=bon_de_commande,
                        product=item["product"],
                        ordered_quantity=item["ordered_quantity"],
                        unit_price=item["unit_price"]
                    )
        except Exception as e:
            print(f"Error saving bon de commande: {e}")
            errors.append("An unexpected error occurred while saving the BonDeCommande. Please try again.")
            return render(request, "purchase/command/bon_de_commande_form.html", {
                "errors": errors,
                "suppliers": suppliers,
                "products": products,
                "product_ids": product_ids,
                "ordered_quantities": ordered_quantities,
                "unit_prices": unit_prices,
                "date": date,
                "time": time
            })

        # Success message and render the confirmation page (or redirect as appropriate)
        messages.success(request, "Bon de commande created successfully.")
        return redirect("bon_de_commande_list")

    # Initial render of the form when GET is requested

    print("list",suppliers)
    return render(request, "purchase/command/bon_de_commande_form.html", {
        "errors": [],
        "suppliers": suppliers,
        "products": products
    })


# List view for BonDeCommande
def bon_de_commande_list(request):
    bon_de_commandes = BonDeCommande.objects.all()
    return render(request, 'purchase/command/bon_de_commande_list.html', {'bon_de_commandes': bon_de_commandes})

# Detail view for BonDeCommande
def bon_de_commande_detail(request, pk):
    bon_de_commande = get_object_or_404(BonDeCommande, pk=pk)
    return render(request, 'purchase/command/bon_de_commande_detail.html', {'bon_de_commande': bon_de_commande})