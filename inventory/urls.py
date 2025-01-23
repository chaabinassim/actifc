from django.urls import path
from django.shortcuts import render
from .views import (
     StoreListView, StoreCreateView, StoreUpdateView,
    CategoryListView, CategoryCreateView, CategoryUpdateView,
    SubCategoryListView, SubCategoryCreateView, SubCategoryUpdateView,
    ProductListView, ProductCreateView, ProductUpdateView,
    render_pdf_view,
    UnitOfMeasurementListView, UnitOfMeasurementCreateView, UnitOfMeasurementUpdateView,
    TechSpecListView, TechSpecCreateView, TechSpecUpdateView,
    MaterialListView, MaterialCreateView, MaterialUpdateView
)

urlpatterns = [
    path('generate-pdf/', render_pdf_view, name='generate_pdf'),
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    
    # SubCategory URLs
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/create/', SubCategoryCreateView.as_view(), name='subcategory-create'),
    path('subcategories/<int:pk>/update/', SubCategoryUpdateView.as_view(), name='subcategory-update'),
    
    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    
    path('stores/', StoreListView.as_view(), name='store_list'),
    path('stores/create/', StoreCreateView.as_view(), name='store_create'),
    path('stores/update/<int:pk>/', StoreUpdateView.as_view(), name='store_update'),

     # UnitOfMeasurement URLs
    path('units/', UnitOfMeasurementListView.as_view(), name='unit-of-measurement-list'),
    path('units/create/', UnitOfMeasurementCreateView.as_view(), name='unit-of-measurement-create'),
    path('units/<int:pk>/update/', UnitOfMeasurementUpdateView.as_view(), name='unit-of-measurement-update'),

    # TechSpec URLs
    path('tech-specs/', TechSpecListView.as_view(), name='tech-spec-list'),
    path('tech-specs/create/', TechSpecCreateView.as_view(), name='tech-spec-create'),
    path('tech-specs/<int:pk>/update/', TechSpecUpdateView.as_view(), name='tech-spec-update'),

    # Material URLs
    path('materials/', MaterialListView.as_view(), name='material-list'),
    path('materials/create/', MaterialCreateView.as_view(), name='material-create'),
    path('materials/<int:pk>/update/', MaterialUpdateView.as_view(), name='material-update'),

    
]
