from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'is_active', 'is_superuser', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    
    


admin.site.register(User, CustomUserAdmin)
admin.site.site_header = "Collaborative Study Portal"
admin.site.site_title = "CSP Admin Portal"
admin.site.index_title = "Welcome to Collaborative Study Portal"
