from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "index.html")


def cleaning(request):
    return render(request, "Cleaning.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.info(request, "password does not match")
            return redirect(request, "register")
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
        return render(request, "register.html")


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
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")

