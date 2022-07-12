from django.shortcuts import redirect, render
from django.http import HttpResponse
from tweets.models import Profile, User
#from django.contrib.auth import login
#Note that the login template already sends a message saying login not successful if invalid credentials are used

def home(request):
    return render(request, 'home.html', context={})


def registration(request):
    return render(request, 'registration.html', context={})

def registration_submit(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    username = request.POST["username"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]

    # Validate username
    same_username = User.objects.filter(username=username).count()
    if same_username > 0:
        err_msg = "Username already exists"
        return render(request, 'registration.html', context={'error': err_msg})

    #Validate password
    if password != confirm_password:
            err_msg = "Your password confirmation did not match your password"
            return render(request, 'registration.html', context={'error': err_msg})

    # Save to database
    u = User.objects.create_user(username, password=password)
    p = Profile(user=u, first_name=first_name, last_name=last_name, email=email)
    p.save()

    return redirect('login')