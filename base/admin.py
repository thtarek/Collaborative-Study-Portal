from django.contrib import admin

from base.models import Todo

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    list_display = ('user','title', 'is_finished', 'created_at')
    ordering = ('-created_at',)
    

admin.site.register(Todo, TodoAdmin)
