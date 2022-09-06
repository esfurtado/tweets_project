
import json
from django.http import HttpResponse
from tweets.models import Tweets

def all_tweets(request):

    tweets = Tweets.objects.all()
    model_dict = {}
    list_dict = []

    for tweet in tweets:
        model_dict = {"user": (tweet.get_user()), "message": (tweet.get_tweet_message()), "post_time": tweet.get_post_time()}
        list_dict.append(model_dict)
    

    

    return HttpResponse(json.dumps(list_dict), content_type="application/json", headers={"Access-Control-Allow-Origin": "http://localhost:3000"})