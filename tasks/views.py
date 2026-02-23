from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, auth
from django.contrib import messages
from .models import House
# from cryptography.fernet import Fernet


# Create your views here.
def home(request):
    return render(request, "homepage/index.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if username == "" or password == "" or confirm_password == "":     #Displays error message if user input is empty
            messages.info(request, "Username or password cannot be empty")
            return redirect("register")
        if password != confirm_password:
            messages.info(request, "password does not match")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.info(request, "username already exists")
            return redirect("register")
        if (
            email and User.objects.filter(email=email).exists()
        ):  # checks email if user input vaLue
            messages.info(request, "email already used")
            return redirect("register")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()  # Creates new user
            return redirect("login")
    else:
        return render(request, "homepage/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(
                request, user
            )  # logs in the user if username and password matched
            return redirect("/")
        else:
            messages.info(request, "Username or password error")
            return redirect("login")
    else:
        return render(request, "homepage/login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def buildhouse(request):
    if request.method == "POST":
        housename = request.POST["housename"]
        if housename == "":
            messages.info(request, "Housename cannot be empty")
            return redirect("buildhouse")
        if House.objects.filter(housename=housename).exists():
            messages.info(request, "House Already Exists")
            return redirect("buildhouse")
        house = House.objects.create(housename=housename)  # Creates a new House
        house.save()
        house.members.add(request.user)  # Adds the current logged in user
        return redirect("enterhouse")       #Redirects to Enterhouse
    else:
        return render(request, "house/buildhouse.html")


def enterhouse(request):
    if request.method=='POST':
        housename = request.POST["housename"]
        if housename == "":
            messages.info(request, "Housename cannot be empty")
            return redirect("enterhouse")
        if not House.objects.filter(housename=housename).exists():
            messages.info(
                request, "House does not exist"
            )  # displays if house does not exist
            return redirect("enterhouse")
        house_id=House.objects.get(housename=housename).id  #assigns the id of housename
        return redirect('house',house_id=house_id)     #Redirects to the house with the id assigned
    else:
        return render(request,'house/enterhouse.html')


def house(request,house_id):
    house=get_object_or_404(House,id=house_id,members=request.user) #Gets the House data if user is the member
    housename=house.housename       
    return render(request, "house/house.html",{'housename':housename,'house_id':house_id})

def cleaning(request,house_id):
    return render(request, "tasks/cleaning.html")

def members(request,house_id):
    return render(request,'house/members.html')

def groceries(request,house_id):
    return render(request,'house/groceries.html')

def plans(request,house_id):
    return render(request,'tasks/plans.html')

def extras(request,house_id):
    return render(request,'tasks/extras.html')