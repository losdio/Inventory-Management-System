from django.contrib.auth.forms import UserCreationForm
from ..forms import SignupForm
from django.urls import reverse_lazy
from django.views.generic import FormView

# Auth view

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')
