from django import forms
from .models import Item, Vendor, Order, User

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'quantity', 'price', 'category', 'vendor_id']
        
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'email', 'phone_number']
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['handled_by', 'status']
        
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address', 'phone_number']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user