from django import forms
from .models import User

class userForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}), error_messages={'required': 'Please enter your first name'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}), error_messages={'required': 'Last name is required'})
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User name'}), error_messages={'required': 'Username is required'})
    email = forms.EmailField( widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}), error_messages={'required': 'Email address is required'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Password'}), error_messages={'required': 'Password is required'})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mt-4', 'placeholder': 'Confirm password'}), error_messages={'required': 'Confirm password is required'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super(userForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError({'confirm_password':'Password does not match.'})
        

        
