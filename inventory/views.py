from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Category, SubCategory, Product,Store
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
    
    


