from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, UserProfileUpdateForm, ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from django.views import View

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'
    
class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'blog/profile.html'

    def get(self, request):
        """Handle GET request - display profile form"""
        user_form = UserProfileUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        """Handle POST request - update profile"""
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })