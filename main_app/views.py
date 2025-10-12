from django.shortcuts import render
from .models import Item
from .forms import ItemForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

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

