from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Items views
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/<int:item_id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Vendors views
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:vendor_id>/', views.VendorDetailView.as_view(), name='vendor_details'),
    path('vendors/create/', views.VendorCreateView.as_view(), name='vendor_create'),
    path('vendors/<int:vendor_id>/update/', views.VendorUpdateView.as_view(), name='vendor_update'),
    path('vendors/<int:vendor_id>/delete/', views.VendorDeleteView.as_view(), name='vendor_delete'),
]
    