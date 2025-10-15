from django.urls import path
from . import views
from .accounts.views import SignupView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Auth
    path('signup/', SignupView.as_view(), name='signup'),
    
    # Items paths
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/<int:item_id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # Vendors paths
    path('vendors/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:vendor_id>/', views.VendorDetailView.as_view(), name='vendor_details'),
    path('vendors/create/', views.VendorCreateView.as_view(), name='vendor_create'),
    path('vendors/<int:vendor_id>/update/', views.VendorUpdateView.as_view(), name='vendor_update'),
    path('vendors/<int:vendor_id>/delete/', views.VendorDeleteView.as_view(), name='vendor_delete'),
    
    # Orders paths
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:order_id>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:order_id>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    
    # Cart paths
    path('cart/<int:cart_id>/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:item_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.CartUpdateView.as_view(), name='update_cart'),
    
    # path('create-admin/', views.create_admin, name='create_admin'),
]
