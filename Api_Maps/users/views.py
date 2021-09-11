"""Users Views."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, response
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import requests

# Mixins
from Api_Maps.mixins import (AjaxFormMixin, form_errors, 
                            re_captcha_validation, redirect_params)

# Models
from .forms import AuthForm, UserForm, ProfileForm


result = 'Error'
message = 'There was an error, please try again.'



class AccountView(TemplateView):
    """Generic FormView with our mixin 
    to display user account page.
    """

    template_name = 'users/account.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def profile_view(request):
    """Handle profile update."""
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)

    if request.is_ajax():
        form = ProfileForm(data=request.POST, instance=profile)
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            result = 'Success'
            message = 'Your profile has been updated.'
        else: 
            message = form_errors(form)
        data = {'result': result, 'message': message}
        return JsonResponse(data)
    else:
        context = {'form': form}
        context = ['google_api_key'] = settings.GOOGLE_API_KEY
        context = ['base_country'] = settings.BASE_COUNTRY
        return render(request, 'users/profile.html', context)


class SignUpView(AjaxFormMixin, FormView):
    """Generic FormView with our mixin for 
    user sign-up with reCAPTCHA security.
    """

    template_name = 'users/sign_up.html'
    form_class = UserForm
    success_url = '/'

    # reCAPTCHA key required in context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha_site_key'] = settings.RECAPTCHA_KEY
        return context

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            token = form.cleaned_data.get('token')
            captcha = re_captcha_validation(token)
            if captcha['success']:
                obj = form.save()
                obj.email = obj.username
                obj.save()
                profile = obj.profile
                profile.captcha_score = float(captcha['score'])

                login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')
                result = 'Success'
                message = 'Thank you for signing up.'
            data = {'result': result, 'message': message}
            return JsonResponse(data)
        return response
