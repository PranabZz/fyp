from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('/authentication/register/')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('/authentication/register/')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('/authentication/register/')

        # Create a new user account
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
        user.save()

        # Tell the user that the accound has been created successfully
        # return HttpResponse('Your account has been created successfully')

        # Log the user in and redirect to the Login page
        messages.success(request, 'Your account has been created successfully')
        return redirect('/authentication/login/')

    return render(request, 'register.html')

def LoginView(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # Log the user in and redirect to the home page
            login(request, user)
            return redirect(reverse('myapp:upload_image'))
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password')

    # Render the login page
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect(reverse('myapp:upload_image'))
