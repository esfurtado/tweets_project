from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('registration', views.registration, name='registration'),
    path('registration/submit', views.registration_submit, name='registration_submit'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit', views.edit, name='edit'),
    path('edit/submit', views.edit_submit, name='edit_submit'),
    path('add/', views.tweet_add, name='tweet_add'),
    path('reply_submit/<int:tweet_id>', views.tweet_reply, name='reply_submit'),
    path('api/all', api.all_tweets, name= 'all_tweets')
]