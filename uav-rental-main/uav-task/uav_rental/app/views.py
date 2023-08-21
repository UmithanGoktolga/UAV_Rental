from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpRequest

from app.forms import UAVForm, RentalForm
from . import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password


# Create your views here.

def home_page(request):
    context  = {'uavs': models.UAV.objects.all(), 'is_authenticated': request.user.is_authenticated}
    print(context)
    return render(request, 'app/index.html', context ) 

#authentication views

def register_page(request: HttpRequest): # register test has made
    if request.method == 'POST':
        name = request.POST.get('name', False)
        surname = request.POST.get('surname', False)
        email = request.POST.get('email', False)
        phone = request.POST.get('phone', False)
        password = make_password(request.POST.get('password', False)) # hashed psw stored in db


        if models.User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return render(request, "app/authentication/register.html")
        else:
            user = models.User(name=name, surname=surname, email=email, phone=phone, password=password)
            user.save()

        return redirect('/')
    else : 
        return render(request, "app/authentication/register.html")


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.utils import timezone



def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Try to fetch the user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Check if user exists and password is correct
        if user is not None and check_password(password, user.password):

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            login(request, user)
            
            print("Am I authenticated?: ", request.user.is_authenticated)
            return redirect("/")
        else:
            messages.error(request, 'Incorrect email or password.')
            return render(request, "app/authentication/login.html")
    
    return render(request, "app/authentication/login.html")


def logout_page(request):
    logout(request)
    return redirect('/')



def uav_form(request, id=0):
    if request.method == "GET":
        if id==0:
            form = UAVForm()
            print("Category Choices:", form.fields['category'].choices)
        else:
            uav = models.UAV.objects.get(pk=id)
            form = UAVForm(instance=uav)
        print("Category Choices:", form.fields['category'].choices)
        return render(request, "app/uav/uav_form.html", {'form': form})
    else:
        if id==0:
            form = UAVForm(request.POST)
            print(form.fields['category'].choices)
        else:
            uav = models.UAV.objects.get(pk=id)
            form = UAVForm(request.POST, instance=uav)
        if form.is_valid():
            form.save()
        return redirect('/')


def uav_delete(request,id):
    uav = models.UAV.objects.get(pk=id)
    uav.delete()
    return redirect('/')



def rental_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = RentalForm()
        else:
            rental = models.Rental.objects.get(pk=id)
            form = RentalForm(instance=rental)
        return render(request, "app/uav/rental_form.html", {'form': form})
    else:
        if id == 0:
            form = RentalForm(request.POST)
        else:
            rental = models.Rental.objects.get(pk=id)
            form = RentalForm(request.POST, instance=rental)
        
        if form.is_valid(): # <-- Here the clean method of the RentalForm gets called
            rental_instance = form.save(commit=False)  # Don't save yet, just get the instance
            
            # Now check for overlaps
            if not rental_instance.is_uav_available():
                messages.error(request, "This UAV is already rented out during the specified period.")
                return render(request, "app/uav/rental_form.html", {'form': form})
            
            rental_instance.save()  # Save only if no overlaps
            return redirect('/rentals')
        else:
            #messages.error(request, "Error: " + ", ".join(form.errors))
            return render(request, "app/uav/rental_form.html", {'form': form})



def rental_delete(request, id):
    rental = models.Rental.objects.get(pk=id)

    if rental.user != request.user:
        messages.error(request, 'You are not authorized to delete this rental.')
        return redirect('/rentals')  # Or wherever you want to redirect

    rental.delete()
    messages.success(request, 'Rental deleted successfully.')
    return redirect('/rentals')


def rentals_list(request):
    rentals = models.Rental.objects.all()
    return render(request, "app/uav/rental_list.html", {'rentals': rentals})



