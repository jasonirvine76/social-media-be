from rest_framework import serializers
from user_api.models import  UserAccount
from socmed_api.models import Feed
from socmed_api.serializers import FeedSerializer

import firebase_admin
import datetime
from firebase_admin import credentials
from firebase_admin import storage

# Firebase Settings
cred = credentials.Certificate("user_api/creds/key.json")
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'ristek-medsos.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)

class UserSerializer(serializers.ModelSerializer):
    feeds = serializers.SerializerMethodField(method_name='get_feeds')
    profile_picture = serializers.SerializerMethodField(method_name='get_picture')
    class Meta:
      model = UserAccount
      fields = ("username","profile_picture","name","bio","close_friends","feeds")

    def get_feeds(self, obj):
        all_feeds = Feed.objects.filter(user=obj)
        list_of_feeds = []
        for feed in all_feeds:
            dct = {}
            dct['id'] = feed.pk
            dct['feed'] = feed.feed_msg
            dct['created_at'] = feed.created_at
            list_of_feeds.append(dct)
        return list_of_feeds

    def get_picture(self, obj):
        try:
            if (obj.profile_picture == ""):
                blob = bucket.blob("static/pp-depresi.jpg")
            else:
                blob = bucket.blob("static/" + str(obj.profile_picture))
                
            url = blob.generate_signed_url(
                    version = "v2",
                    expiration=datetime.timedelta(days=365), 
                    method='GET')
            return url
        except:
            return None
    
class AllUsernameSerializer(serializers.ModelSerializer):
    is_close_friends = serializers.SerializerMethodField(method_name='check_close_friends')
    class Meta:
        model = UserAccount
        fields = ("username","is_close_friends",)

    def check_close_friends(self, obj):
        userLogged = UserAccount.objects.get(username=self.context.user)
        if (obj in userLogged.close_friends.all()):
            return True
        return False
    
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("name","bio","profile_picture")
