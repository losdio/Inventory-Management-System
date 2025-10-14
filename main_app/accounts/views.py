from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from ..forms import SignupForm
from django.urls import reverse_lazy
from django.views.generic import FormView

# Auth view

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})