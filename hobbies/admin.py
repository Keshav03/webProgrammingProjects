from django.contrib import admin

# Register your models here.

from hobbies.models import FriendList, FriendsRequest, Profile, Hobby, User

admin.site.register(Profile)
admin.site.register(Hobby)
admin.site.register(User)
admin.site.register(FriendList)
admin.site.register(FriendsRequest)