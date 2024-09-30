from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            print(user)
            return redirect('home')
    return render(request, 'index.html')

def home(request):
    return render(request,'home.html')


