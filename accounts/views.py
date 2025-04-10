from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .documents import Account
from django.contrib.auth.hashers import make_password

def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, 'accounts/login.html', {'template_data': {'title': 'Login'}})


@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('homepage')


def signup(request):
    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        email      = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        error = None
        if not all([username, email, first_name, last_name]):
            error = "All fields are required."
        elif password != password2:
            error = "Passwords do not match."
        elif Account.objects(username=username).first():
            error = "Username already exists."
        elif Account.objects(email=email).first():
            error = "Email already exists."

        if error:
            messages.error(request, error)
            return render(request, 'accounts/signup.html', {'template_data': {'title': 'Sign Up'}})

        acct = Account(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=make_password(password)
        )
        acct.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('accounts:login')

    return render(request, 'accounts/signup.html', {'template_data': {'title': 'Sign Up'}})
