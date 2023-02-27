from rest_framework import serializers
from socmed_api.models import Feed
from rest_framework.exceptions import AuthenticationFailed
from user_api.models import UserAccount

import firebase_admin
import datetime
from firebase_admin import credentials
from firebase_admin import storage

# Firebase Settings
cred = credentials.Certificate("user_api/creds/key.json")
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'ristek-medsos.appspot.com',
}, name='storage-feed')

bucket = storage.bucket(app=app)

def get_picture_url(pic_name):
        try:
            if (pic_name == ""):
                blob = bucket.blob("static/pp-depresi.jpg")
            else:
                blob = bucket.blob("static/" + str(pic_name))
                
            url = blob.generate_signed_url(
                    version = "v2",
                    expiration=datetime.timedelta(days=365), 
                    method='GET')
            return url
        except:
            return None

class GetFeedSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_feeds')
    class Meta:
        model = Feed
        fields = ('data',)

    def get_feeds(self, obj):
        filtered_feeds = []
        list_of_feeds = Feed.objects.all()
        try:
            user_login = UserAccount.objects.get(username=self.context.user)
            for feed in list_of_feeds:
                creator = UserAccount.objects.get(username=feed.user)
                profile_picture = get_picture_url(str(creator.profile_picture))

                if user_login in creator.close_friends.all():
                    dct = {}
                    dct['id'] = feed.pk
                    dct['profile_picture'] = profile_picture
                    dct['user'] = creator.username
                    dct['feed_msg'] = feed.feed_msg
                    dct['created_at'] = feed.created_at
                    dct['visibility_to_close_friends'] = feed.visibility_to_close_friends

                else:
                    if feed.visibility_to_close_friends != True:
                        dct = {}
                        dct['id'] = feed.pk
                        dct['profile_picture'] = profile_picture
                        dct['user'] = creator.username
                        dct['feed_msg'] = feed.feed_msg
                        dct['created_at'] = feed.created_at
                        dct['visibility_to_close_friends'] = feed.visibility_to_close_friends
                filtered_feeds.append(dct)
        except:
            for feed in list_of_feeds:
                if feed.visibility_to_close_friends != True:
                    dct = {}
                    creator = UserAccount.objects.get(username=feed.user)
                    profile_picture = get_picture_url(str(creator.profile_picture))
                    dct['id'] = feed.pk
                    dct['profile_picture'] = profile_picture
                    dct['user'] = UserAccount.objects.get(username = feed.user).username
                    dct['feed_msg'] = feed.feed_msg
                    dct['created_at'] = feed.created_at
                    dct['visibility_to_close_friends'] = feed.visibility_to_close_friends
                    filtered_feeds.append(dct)
            
        return filtered_feeds
    
    
    
class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('user','feed_msg', 'visibility_to_close_friends')

    

    
                

    

