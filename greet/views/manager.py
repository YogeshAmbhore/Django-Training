from django import forms
from django import contrib
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.base import Model
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, models
from django.contrib import messages
from django.urls.conf import path
from greet.models import PMProfile, Ticket, User
from greet.forms import ManagerCreationForm, TicketForm, TicketUpdationForm, UserLoginForm


from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse

class IndexView(TemplateView):
    template_name = 'greet/home.html'


class ManagerLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'greet/pmlogin.html'
    page = 'pmlogin'
    extra_context = {'page': page}

    def get_success_url(self):
        if self.request.user.is_manager:
            return reverse('pmdashboard')
        return super().get_success_url()



def logoutmanager(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('pmlogin')


class RegisterManager(CreateView):
    template_name = 'greet/pmlogin.html'
    form_class = ManagerCreationForm
    model = User
    page = 'pmsignup'
    extra_context = {'page': page}
    success_url = reverse_lazy('pmlogin')


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'greet.view_pmprofile'
    extra_context = {'page': 'dashboard'}
    template_name = 'greet/managerdashboard.html'
    # login_url = "pmlogin"


class AllTicketView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('greet.view_pmprofile', 'greet.view_ticket')
    template_name = 'greet/alltickets.html'

    def get_context_data(self, **kwargs):
        context = super(AllTicketView, self).get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status', 'Open')
        if context['status'] == 'Open':
            context['tickets'] = Ticket.objects.filter(status = 'Open')
        else:
            context['tickets'] = Ticket.objects.filter(status__iexact=context['status'], user=self.request.user.pmprofile)
        return context


class CreateTicketView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('greet.add_ticket')
    template_name = 'greet/ticket_create.html'
    form_class = TicketForm
    page = 'createtickets'
    extra_context = {'page': page}
    success_url = reverse_lazy('pmdashboard')

    def form_valid(self, form):
        # form.fields['status'].widget = forms.HiddenInput()
        form.instance.user = self.request.user.pmprofile
        return super().form_valid(form)


class UpdateTicketView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('greet.view_pmprofile', 'greet.change_ticket')
    template_name = 'greet/ticket_create.html'
    form_class = TicketUpdationForm
    page = 'updateticket'
    extra_context = {'page': page}
    success_url = reverse_lazy('pmdashboard')

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self, form):
        if form.instance.status == 'Open':
            form.instance.accessed_by = None
        # form.instance.user = self.request.user.pmprofile
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
