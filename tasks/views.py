from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, auth
from django.contrib import messages
from .models import House, Cleaning_Task
from datetime import date, datetime

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

        if (
            username == "" or password == "" or confirm_password == ""
        ):  # Displays error message if user input is empty
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
        return redirect("enterhouse")  # Redirects to Enterhouse
    else:
        return render(request, "house/buildhouse.html")


def enterhouse(request):
    if request.method == "POST":
        housename = request.POST["housename"]
        house_id = request.POST["house_id"]

        if housename == "" or house_id == "":
            messages.info(request, "Fields cannot be empty")
            return redirect("enterhouse")

        if not House.objects.filter(housename=housename, id=house_id).exists():
            messages.info(
                request, "Incorrect House name or id"
            )  # displays if house does not exist
            return redirect("enterhouse")

        if not House.objects.filter(members=request.user).exists():
            messages.info(request, "Your are not a member, Request to join")
            return redirect("enterhouse")

        house = House.objects.get(
            housename=housename, id=house_id
        )  # assigns the house of housename
        return redirect(
            "house", house_id=house_id
        )  # Redirects to the house with the id assigned
    else:
        return render(request, "house/enterhouse.html")


def request_join(request):
    if request.method == "POST":
        housename = request.POST["housename"]
        house_id = request.POST["house_id"]

        if housename == "" or house_id == "":
            messages.info(request, "Fields cannot be empty")
            return redirect("request_join")

        if not House.objects.filter(housename=housename, id=house_id).exists():
            messages.info(
                request, "Incorrect House name or id"
            )  # displays if house does not exist
            return redirect("request_join")
        house = House.objects.get(housename=housename, id=house_id)
        if house.members.filter(
            id=request.user.id
        ).exists():  # loops through members to check if they are a member or not
            messages.info(request, "You already are a member of this house")
            return redirect("request_join")
        house.request.add(request.user)  # Adds to the request list
        messages.success(request, "Request sent successfully")
        return redirect("request_join")

    else:
        return render(request, "house/request_join.html")


def house(request, house_id):
    house_details = get_object_or_404(
        House, id=house_id, members=request.user
    )  # Gets the House data if user is the member
    housename = house_details.housename
    return render(
        request, "house/house.html", {"housename": housename, "house_id": house_id}
    )


def cleaning(request, house_id):
    if request.method=='POST':
        house=get_object_or_404(House,id=house_id,members=request.user)
        task_name=request.POST['task_name']
        description=request.POST['description']
        task=request.POST.get("task")
        assigned_members= request.POST.getlist("assigned_members[]")
        date_today=date.today()                 #   Date
        date_=date_today.isocalendar()           #Datefield
        week=date_.week

        if task=='add':             #adds tasks if user presses add task button
            if task_name=='' or description=='':
                messages.error(request, 'Task name or Description cannot be empty')
                return redirect('cleaning',house_id)
            if not assigned_members:
                messages.error(request,'Assign members')
                return redirect('cleaning',house_id)
            new_task=Cleaning_Task.objects.create(name=task_name,description=description,user_added=request.user,date=datetime.now(),House=house_id,start_week=week)
            for member in assigned_members:
                new_task.assigned_members.add(member)
            messages.success(request,'Task added sucessfully')
            return redirect('cleaning',house_id)

    else:
        house=get_object_or_404(House,id=house_id,members=request.user) #Gets the house from models with specific houseId if user is on of the member
        tasks_data=Cleaning_Task.objects.filter(House=house_id) #Gets the tasks_data
        tasks=[]
        for task in tasks_data:
            tasks.append({'task': task,'assigned_members':task.assigned_members.all()})
        members=house.members.all()
        return render(request, "tasks/cleaning.html",{'members':members,'tasks':tasks,'house_id':house_id})

def task_action(request, house_id):     #Actions to be performed on tasks (UD) OF CRUD
    action=request.POST.get('task_action')
    tasks=request.POST.getlist('task_action[]')
    cleaning = Cleaning_Task.objects.filter(House=house_id)
    delete = request.POST.get('delete')

    if action=='':
        messages.error(request,'Select Action to perform')
        return redirect('cleaning',house_id)
    if not tasks:
        messages.error(request,'Select tasks to perform actions')
        return redirect('cleaning',house_id)

    #Renders edit_task page
    elif action=='edit':
        tasks_to_edit=[]
      
        for task in tasks:
            house_task=cleaning.get(id=task)
            house=House.objects.get(id=house_id)
            house_members = house.members.all()
            task_members = house_task.assigned_members.all()    
            #Gets members that are not assigned to the task
            not_assigned_members = list(set(task_members) ^ set(house_members))
            tasks_to_edit.append({'task': house_task, 'not_assigned_members':not_assigned_members})
        return render(request,'tasks/edit_task.html',{'tasks' : tasks_to_edit})
    if delete=="yes":
        for task in tasks:
            task_to_delete = cleaning.get(id=task)
            task_to_delete.delete()
        messages.success(request,'successfully deletd tasks')
        return redirect('cleaning',house_id)
    if action=='done':
        for task_id in tasks:
            task_to_mark = cleaning.get(id=task_id)
            task_to_mark.done=True
            task_to_mark.save()
        messages.success(request,'Tasks marked done')
        return redirect('cleaning',house_id)
    if action=='unmark_done':
        for task_id in tasks:
            task_to_unmark=cleaning.get(id=task_id)
            task_to_unmark.done=False
            task_to_unmark.save()
        messages.success(request,'Tasks unmarked done')
    return redirect('cleaning',house_id)


def edit_task(tasks):
    pass

    


def members(request, house_id):
    if request.method == "POST":
        member_id = request.POST.getlist("member[]")
        members_action = request.POST.get("action")
        join_request = request.POST.get("join_request")
        member_request = request.POST.getlist(
            "member_request[]"
        )  # gets list of checked members
        house = House.objects.get(id=house_id)  # Selects house_id

        if members_action == "remove_members":
            for member in member_id:
                house.members.remove(member)

        if join_request == "add_members":  # If user pressed add members
            for member in member_request:
                house.members.add(member)  # Adds selected user to the members list
                house.request.remove(member)  # Removes request
        elif join_request == "reject_request":
            for member in member_request:
                house.request.remove(member)  # Rejects join request
        return redirect("members", house_id=house_id)
    else:
        house = get_object_or_404(House, id=house_id, members=request.user)
        members = house.members.all()  # Gets all the house members
        requests = house.request.all()  # Gets the user requests
        return render(
            request, "house/members.html", {"members": members, "requests": requests}
        )

