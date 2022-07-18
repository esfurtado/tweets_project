from django.db import models
from django.contrib.auth.models import User

# Note that the user model has already been created with django auth
# So we use the OneToOneField class to store extra information required for the registration of the tweets app
# OneToOneField creates a foreign key that connects the Profile table to the user table from Django
#Idea taken from https://simpleisbetterthancomplex.com

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    contact_number = models.CharField(max_length=30)

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_message = models.TextField(max_length=144)
    post_time = models.DateTimeField(auto_now_add=True)

    def all_replies(self):
        return TweetsReplies.objects.filter(tweet_id=self.id)
    
class TweetsReplies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_message = models.TextField(max_length=144)
    post_time = models.DateTimeField(auto_now_add=True)
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE)

