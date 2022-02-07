from django.db import models
from django import forms
from django.forms import ModelForm, fields
from django.contrib.auth.models import Group
# from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PMProfile, DevProfile, User, Ticket


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


class ManagerCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise forms.ValidationError("the given username is already registered")
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name' : 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(ManagerCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        manager = PMProfile.objects.create(user=user)
        group = Group.objects.get(name='manager')
        user.groups.add(group)
        return user


class DeveloperCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise forms.ValidationError("the given username is already registered")
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']
        
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name' : 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(DeveloperCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        developer = DevProfile.objects.create(user=user)
        group = Group.objects.get(name='developer')
        user.groups.add(group)
        return user


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
        labels = {
            'title' : 'Title',
            'description' : 'Description',
            'status' : 'Status'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class TicketUpdationForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status']
        labels = {
            'title' : 'Title',
            'description' : 'Description',
            'status' : 'Update Status'
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if self.user.is_developer:
            self.fields['status'] = forms.ChoiceField(label=('Update Status'), 
                               choices=(('Accepted', ('Accepted')), 
                                        ('Completed', ('Completed'))))
        
        elif self.user.is_manager:
            self.fields['status'] = forms.ChoiceField(label=('Update Status'), 
                               choices=(('Accepted', ('Accepted')), 
                                        ('Completed', ('Completed')),
                                        ('Closed', ('Closed'))))

        # print(self.fields['status'])
        # print(type(self.fields['status']))

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

