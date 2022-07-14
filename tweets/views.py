from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from tweets.models import Profile, User

#from django.contrib.auth import login
#Note that the login template already sends a message saying login not successful if invalid credentials are used

def home(request):
    return render(request, 'home.html', context={})


def registration(request):
    #if user is already registered they can edit their details
    #if not they can register and create a new profile
    if request.user.is_authenticated:
        return redirect('edit')
    else:
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

    # Validate password
    if password != confirm_password:
            err_msg = "Your password confirmation did not match your password"
            return render(request, 'registration.html', context={'error': err_msg})
    
    # Validate email
    same_email = User.objects.filter(email=email).count()
    if same_email > 0:
        err_msg = "You already have an account with this email"
        return render(request, 'registration.html', context={'error': err_msg})

    # Save to database
    u = User.objects.create_user(username, password=password)
    p = Profile(user=u, first_name=first_name, last_name=last_name, email=email)
    p.save()

    return redirect('login')


def profile(request, username):
    if request.user.username == username:
        return render(request, 'profile.html',context={})
    else:
        raise PermissionDenied()


def edit(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user_id=user.id)

        return render(request, 'edit.html', context={ 'profile': profile })
            # 'current_firstname': profile.first_name, 'current_lastname:': profile.last_name, 'current_email': profile.email, 'current_contact': profile.contact_number})
    else:
        return redirect('login')


def edit_submit(request):
    new_firstname = request.POST["new_firstname"]
    new_lastname = request.POST["new_lastname"]
    new_email = request.POST["new_email"]
    new_contact = request.POST["new_contact"]

    print(f"{new_lastname}")
    user = request.user
    profile : Profile = Profile.objects.get(user_id=user.id)
    
    #If user changed a field, save to database, otherwise do nothing
    if new_firstname !='':
        profile.first_name = new_firstname
 
    if new_lastname != '':
        profile.last_name = new_lastname
    
    if new_email !='':
        profile.email = new_email
    
    if new_contact !='':
        profile.contact_number = new_contact

    profile.save()
    return redirect('profile', user.username)

