from django import forms
from django import contrib
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic.edit import CreateView
from greet.models import DevProfile, Ticket, User
from greet.forms import DeveloperCreationForm, TicketUpdationForm, UserLoginForm

from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.views import LoginView

from greet.views.manager import CreateTicketView
from django.urls import reverse


class DevDashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'greet.view_devprofile'
    extra_context = {'page': 'dashboard'}
    template_name = 'greet/developerdashboard.html'


class DeveloperLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'greet/devlogin.html'
    page = 'devlogin'
    extra_context = {'page': page}

    def get_success_url(self):
        if self.request.user.is_developer:
            return reverse('devdashboard')

        return super().get_success_url()


def logoutdevloper(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('devlogin')


class RegisterDeveloper(CreateView):
    template_name = 'greet/devlogin.html'
    form_class = DeveloperCreationForm
    model = User
    page = 'devsignup'
    extra_context = {'page': page}
    success_url = reverse_lazy('devlogin')


class DevTicketView(LoginRequiredMixin,  PermissionRequiredMixin, TemplateView):
    permission_required = ('greet.view_devprofile', 'greet.view_ticket')
    template_name = 'greet/ticket_list.html'

    def get_context_data(self, **kwargs):
        context = super(DevTicketView, self).get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status', 'Open')
        if context['status'] == 'Open':
            context['tickets'] = Ticket.objects.filter(status = 'Open')
        else:
            context['tickets'] = Ticket.objects.filter(status__iexact=context['status'], accessed_by=self.request.user.devprofile)
        return context


class DevUpdateTicketView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('greet.view_devprofile', 'greet.change_ticket')
    template_name = 'greet/ticket_create.html'

    form_class = TicketUpdationForm
    page = 'updateticket'
    extra_context = {'page': page}
    success_url = reverse_lazy('devdashboard')

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self, form):
        form.instance.accessed_by = self.request.user.devprofile
        return super().form_valid(form)
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

