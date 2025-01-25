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
    MaterialListView, MaterialCreateView, MaterialUpdateView,
    ProjectListView, ProjectCreateView, ProjectUpdateView,
    create_supply_demand,supply_demand_list,supply_demand_detail,
    create_supply_demand_review,supply_demand_review_list,supply_demand_review_detail,
    create_supply_order,supply_order_list,supply_order_detail,
    create_purchase_demand,purchase_demand_list,purchase_demand_detail,purchase_demand_pdf,
    create_bon_de_commande,bon_de_commande_list,bon_de_commande_detail,
    
    
    
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

    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),

    path('supply-demands/create/', create_supply_demand, name='supply-demand-create'),
    path('supply-demands/', supply_demand_list, name='supply-demand-list'),
    path('supply-demand/<int:pk>/', supply_demand_detail, name='supply-demand-detail'),


    path('supply-reviews/create/<int:supply_demand_id>/', create_supply_demand_review, name='create_supply_demand_review'),
    path('supply-reviews/',supply_demand_review_list , name='supply-demand-review-list'),
    path('supply-demand-review/<int:pk>/', supply_demand_review_detail, name='supply-demand-review-detail'),
    
    path('supply-orders/create/<int:supply_demand_review_id>/', create_supply_order, name='create_supply_order'),
    path('supply-orders/', supply_order_list, name='supply_order_list'),
    path('supply-orders/<int:supply_order_id>/', supply_order_detail, name='supply_order_detail'),

    path("purchase-demand/create/",create_purchase_demand, name="create-purchase-demand"),
    path("purchase-demand/", purchase_demand_list, name="purchase-demand-list"),
    path("purchase-demand/<int:pk>/", purchase_demand_detail, name="purchase-demand-detail"),
    path('purchase-demand/pdf/<int:pk>/', purchase_demand_pdf, name='purchase_demand_pdf'),

    path('purchase-command/create/<int:purchase_demand_id>/', create_bon_de_commande, name='create_bon_de_commande'),
    path('purchase-commande/', bon_de_commande_list, name='bon_de_commande_list'),
    path('purchase-commande/<int:pk>/', bon_de_commande_detail, name='bon_de_commande_detail'),
    
]
