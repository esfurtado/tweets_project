# POST

What does POST do on views.py?

* Firstly we need a **form** - this is created inside the templates folder in html file with the tag form.
* Everything within that form will have a key with the values to be inserted by the user
* When views.py uses POST it accesses the dictionary as per example below, where we access the username:

```python
    username = request.POST["username"]
```

Why is this important? Now that we get access to what the user wrote we can:
* Validate (for example find whether it already exists)
* Save it into the database

# Models and Django's auth

The classes within models will contain the attributes that relate to the data we want to save, such as username, password, or email.

**Importing User from django.contrib.auth.models** - We need to use the User from django's auth as this allows us to login

Note that we use the template with login and don't need to write a view for it to be rendered. This is Django's background magic happening that already has its own views. However, for this to work we still need to add a url path for the django.auth and a Redirect on settings.

Here I've built my own table to be populated with the registration form's attributes so I can query that table directly and change it more easily than the User's table. This is linked with Django's user table with OneToOneField.

**User.objects** - This a special Django ORM module that interacts with the user table so we can query it the same way we would use Squlite to filter, count or populate table.

# How to configure URLs
We have two URLs folders - one for the project and one for the app.

Firstly, the project URLs folder keeps track of the admin url. The admin url locates the admin page and that also needs a superuser for login. To create a superuser use the command line - python manage.py createsuperuser.

As we are using django auth for login, we also created a path called 'auth/' which includes the urls from django.contrib.urls.

The most important for the app itself is the main url which then locates all subsquent urls for the app. In this case I named it 'tweets/' and then include tweets.urls to point it to the the tweets app folder.

The home page has an empty path as the first url of the tweets app.
This is so that if we select /tweets/ it goes directly to the home page. All other paths will be /tweets/othername. As per code below note they also contain their view and a name. The name is used to make links on the templates.

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('registration', views.registration, name='registration'),
    path('registration/submit', views.registration_submit, name='registration_submit')
```



