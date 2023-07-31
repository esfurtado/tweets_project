from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from tweets.models import Profile, TweetsReplies, User, Tweets

import logging

logger = logging.getLogger('tweets')

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
    same_email = Profile.objects.filter(email=email).count()
    if same_email > 0:
        err_msg = "You already have an account with this email"
        return render(request, 'registration.html', context={'error': err_msg})

    # Save to database
    u = User.objects.create_user(username, password=password)
    p = Profile(user=u, first_name=first_name, last_name=last_name, email=email)
    p.save()
    logger.info(f'User {u.username} saved to database')

    return redirect('login')


def profile(request, username):
    user = request.user
    if request.user.username == username:
        tweet_messages = Tweets.objects.all().filter(user_id=user.id)[:10]
        return render(request, 'profile.html',context={'tweet_messages':tweet_messages})
    else:
        raise PermissionDenied()


def edit(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user_id=user.id)

        return render(request, 'edit.html', context={ 'profile': profile })
    else:
        return redirect('login')


def edit_submit(request):
    new_firstname = request.POST["new_firstname"]
    new_lastname = request.POST["new_lastname"]
    new_email = request.POST["new_email"]
    new_contact = request.POST["new_contact"]

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


def tweet_add(request):
    #post message
    new_tweet = request.POST['new_tweet']
    #save message to database
    user= request.user
    tweet_message = Tweets(user=user, tweet_message=new_tweet)
    tweet_message.save()
    logger.info(f'User {user.username} posted: {tweet_message.tweet_message}')
    
    return redirect('profile', user.username)

def tweet_reply(request, tweet_id):
    #add reply message
    new_reply = request.POST['reply']
    tweet = Tweets.objects.get(id=tweet_id)
    #save reply to database
    user = request.user
    tweet_reply = TweetsReplies(user=user, tweet_message=new_reply, tweet=tweet)
    tweet_reply.save()
    logger.info(f'User {user.username} replied: {tweet_reply.tweet_message} on tweet with id {tweet.id}')

    return redirect('profile', user.username)