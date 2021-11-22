from django import forms
from django import contrib
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, models
from django.contrib import messages
from django.urls.conf import path
from greet.models import PMProfile, Ticket
from greet.forms import ManagerCreationForm, TicketForm


from django.views.generic import TemplateView, ListView, CreateView, UpdateView

class IndexView(TemplateView):
    template_name = 'greet/home.html'


def loginmanager(request):
    page = 'pmlogin'

    if request.user.is_authenticated:
        return redirect('pmdashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = PMProfile.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_manager:
            login(request, user)
            return redirect('pmdashboard')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'greet/pmlogin.html')


def logoutmanager(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('pmlogin')


def signupmanager(request):
    page = 'pmsignup'
    form = ManagerCreationForm()

    if request.user.is_authenticated:
        return redirect('pmdashboard')

    if request.method == 'POST':
        form = ManagerCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('pmlogin')

        else:
            messages.success(request, 'An error has occured during registration')

    context = {'page': page, 'form': form}
    return render(request, 'greet/pmlogin.html', context)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'greet/managerdashboard.html'

class AllTicketView(LoginRequiredMixin, ListView):
    template_name = 'greet/alltickets.html'
    model = Ticket
    page = 'alltickets'
    extra_context = {'page': page}

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user.pmprofile)
        return queryset


class OpenTicketView(LoginRequiredMixin, ListView):
    # model = Ticket
    template_name = 'greet/alltickets.html'
    model = Ticket
    page = 'opentickets'
    extra_context = {'page' : page}

    def get_queryset(self):
        queryset = Ticket.objects.filter(status = 'Open')
        return queryset


class AcceptedTicketView(LoginRequiredMixin, ListView):
    template_name = 'greet/alltickets.html'
    model = Ticket
    page = 'acceptedtickets'
    extra_context = {'page' : page}

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user.pmprofile, status = 'Accepted')
        return queryset


class CompletedTicketView(LoginRequiredMixin, ListView):
    template_name = 'greet/alltickets.html'
    model = Ticket
    page = 'completedtickets'
    extra_context = {'page': page}

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user.pmprofile, status = 'Completed')
        return queryset


class ClosedTicketView(LoginRequiredMixin, ListView):
    template_name = 'greet/alltickets.html'
    model = Ticket
    page = 'closedtickets'
    extra_context = {'page': page}

    def get_queryset(self):
        queryset = Ticket.objects.filter(user=self.request.user.pmprofile, status = 'Closed')
        return queryset


class CreateTicketView(LoginRequiredMixin, CreateView):
    template_name = 'greet/ticket_create.html'
    form_class = TicketForm
    page = 'createtickets'
    extra_context = {'page': page}
    success_url = reverse_lazy('opentickets')

    def form_valid(self, form):
        form.instance.user = self.request.user.pmprofile
        return super().form_valid(form)


class UpdateTicketView(LoginRequiredMixin, UpdateView):
    template_name = 'greet/ticket_create.html'
    form_class = TicketForm
    page = 'updateticket'
    extra_context = {'page': page}
    success_url = reverse_lazy('opentickets')

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Ticket, id=id_)

    def form_valid(self, form):
        if form.instance.status == 'Open':
            form.instance.accessed_by = None
        # form.instance.user = self.request.user.pmprofile
        return super().form_valid(form)