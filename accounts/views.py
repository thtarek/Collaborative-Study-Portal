from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import redirect

from django.http import HttpResponse


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

def user_logout(request):
    auth.logout(request)
    return redirect('user_login')
