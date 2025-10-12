from django.shortcuts import render
from .models import Item, Vendor
from .forms import ItemForm, VendorForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
# Item views

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'item_id'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')

class ItemUpdateView(UpdateView):  
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'

# Vendor views

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendors/vendor_list.html'
    context_object_name = 'vendors'
    
class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'vendors/vendor_detail.html'
    context_object_name = 'vendor'
    pk_url_kwarg = 'vendor_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.get_object()
        context['items'] = Item.objects.select_related('vendor_id').filter(vendor_id=vendor.id)
        return context

class VendorCreateView(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')

class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')
    pk_url_kwarg = 'vendor_id'

class VendorDeleteView(DeleteView):
    model = Vendor
    success_url = reverse_lazy('vendor_list')
    pk_url_kwarg = 'vendor_id'
    
