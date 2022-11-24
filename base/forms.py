from django import forms
from .models import Todo
from django.forms import ModelForm, TextInput, EmailInput

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control form-control-lg mr-5'}),
        }
