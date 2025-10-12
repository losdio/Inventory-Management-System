from django import forms
from .models import Item, Vendor

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'quantity', 'price', 'category', 'vendor_id']
        
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'email', 'phone_number']