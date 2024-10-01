from django.shortcuts import render, redirect
from django.contrib.auth import login as login_django
from django.contrib.auth import authenticate


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login_django(request, user)
            return redirect('home')
    return render(request, 'index.html')

def home(request):
    return render(request,'home.html')


