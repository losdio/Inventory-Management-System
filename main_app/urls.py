from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/<int:item_id>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:item_id>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:item_id>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
]