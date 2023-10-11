
from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from requests.exceptions import RequestException
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST':
        item_id = request.POST.get('order')
        # Call warehouse API to order item
        response = requests.post(f'http://127.0.0.1:8080/api/order/{item_id}/', headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Raise HTTPError for bad responses
        if response.json()['status'] == 'success':
            # Optionally, update local items list or redirect
            return redirect('index')
        else:
            messages.error(request, 'No items left.')

    
    items = requests.get('http://127.0.0.1:8080/api/items/').json()['items']
    return render(request, 'index.html', {'items': items})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
