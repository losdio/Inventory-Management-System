from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from .models import Item, User, Vendor, Order, OrderItem, Cart, CartItem
from .forms import ItemForm, VendorForm, OrderForm
from .core.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib import messages

# Home view

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

class ItemCreateView(RoleRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')
    allowed_roles = ['admin']

class ItemUpdateView(RoleRequiredMixin, UpdateView):  
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'
    allowed_roles = ['admin', 'staff']
    

class ItemDeleteView(RoleRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('item_list')
    pk_url_kwarg = 'item_id'
    allowed_roles = ['admin']

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

class VendorCreateView(RoleRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')
    allowed_roles = ['admin']

class VendorUpdateView(RoleRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'
    success_url = reverse_lazy('vendor_list')
    pk_url_kwarg = 'vendor_id'
    allowed_roles = ['admin']

class VendorDeleteView(RoleRequiredMixin, DeleteView):
    model = Vendor
    success_url = reverse_lazy('vendor_list')
    pk_url_kwarg = 'vendor_id'
    allowed_roles = ['admin']
    
# Order views

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('item_id', 'quantity'), extra=1, can_delete=True)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['orderitems'] = OrderItem.objects.select_related('order_id').filter(order_id=order.id)
        return context

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('cart_detail', cart_id=Cart.objects.get(user_id=request.user).id)
    def post(self, request):
        allowed = True
        cart = Cart.objects.get(user_id=request.user)
        for ci in cart.cartitem_set.all():
            item = Item.objects.get(id=ci.item_id.id)
            if item.quantity < ci.quantity:
                messages.error(request, f"Not enough stock for {item.item_name}.")
                allowed = False
                return redirect('cart_detail', cart_id=cart.id)
        order = Order.objects.create(user_id=request.user, total_price=cart.total_price(), status=Order.Status.PENDING)
        if allowed:
            for ci in cart.cartitem_set.all():
                item = Item.objects.get(id=ci.item_id.id)
                OrderItem.objects.create(order_id=order, item_id=ci.item_id, quantity=ci.quantity, price=ci.item_id.price)
                item.quantity -= ci.quantity
                item.save()
            cart.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_list')

class OrderUpdateView(RoleRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')
    pk_url_kwarg = 'order_id'
    allowed_roles = ['staff', 'admin']

class OrderDeleteView(RoleRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')
    pk_url_kwarg = 'order_id'
    allowed_roles = ['staff', 'admin']

# Cart views

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = Item.objects.get(id=item_id)
        cart, created = Cart.objects.get_or_create(user_id=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart_id=cart, item_id=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart_detail', cart_id=cart.id)

class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'cart/cart_detail.html'
    context_object_name = 'cart'
    pk_url_kwarg = 'cart_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object()
        context["cart_items"] = CartItem.objects.filter(cart_id=cart.id)
        return context
    
class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = Cart.objects.get(user_id=request.user)
        item = Item.objects.get(id=item_id)
        cart_item = CartItem.objects.get(cart_id=cart, item_id=item)
        cart_item.delete()
        return redirect('cart_detail', cart_id=cart_item.cart_id.id)

class CartUpdateView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = Cart.objects.get(user_id=request.user)
        item = Item.objects.get(id=item_id)
        cart_item = CartItem.objects.get(cart_id=cart, item_id=item)
        quantity = request.POST.get('quantity')
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            return redirect('remove_from_cart', item_id=item)
        return redirect('cart_detail', cart_id=cart_item.cart_id.id)
    

from django.http import HttpResponse

# def create_admin(request):
#     if not User.objects.filter(username="admin").exists():
#         User.objects.create_superuser(
#             username="admin",
#             email="admin@example.com",
#             password="admin123"
#         )
#         return HttpResponse("Superuser created successfully!")
#     else:
#         return HttpResponse("Superuser already exists.")