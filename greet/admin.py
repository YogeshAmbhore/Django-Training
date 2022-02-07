from django.contrib import admin
from django.forms import models
from .models import PMProfile, DevProfile, User, Ticket
from django.contrib.auth.admin import UserAdmin
from .forms import DeveloperCreationForm, TicketForm
# from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = DeveloperCreationForm
    model = User
    list_display = ('email', 'first_name', 'is_staff', 'is_active', 'is_manager', 'is_developer')
    list_filter = ('email', 'first_name', 'is_staff', 'is_active', 'is_manager', 'is_developer')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_manager', 'is_developer', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_manager', 'is_developer'),
        }),
    )

    search_fields = ('email', 'first_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

admin.site.register(PMProfile)
admin.site.register(DevProfile)
admin.site.register(Ticket)