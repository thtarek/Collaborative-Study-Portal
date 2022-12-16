from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import redirect

from django.http import HttpResponse

from accounts.forms import userForm
from accounts.models import User


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid email or password.')
            return redirect('user_login')
    return render(request, 'accounts/login.html')

@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'portal/dashboard.html')

@login_required(login_url='user_login')
def user_logout(request):
    auth.logout(request)
    return redirect('user_login')

def create_account(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        # print(request.POST)
        form = userForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            user.is_active = False
            user.save()
            messages.success(request, 'Your account created successfully! Wait for admin approve!')
            return redirect('user_login')
        else:
            print(form.errors)
    else:
        form = userForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/create_account.html', context)
