"""group_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from hobbies.api import profiles_api, users_api , send_request_api, view_friends_request_api, accept_friend_request_api, decline_friend_request_api, view_friends_api, remove_friend_api, profile_api

from django.contrib import admin
from django.urls import include, path

from django.conf.urls.static import static;
from django.conf import settings;


urlpatterns = [

    path('health/', lambda request: HttpResponse("OK")),

    path('', include('hobbies.urls')), 

    path('admin/', admin.site.urls),

    path('api/profiles/', profiles_api, name="profiles api"),

    path('api/users/', users_api, name="users api"),

    path('api/sendRequest', send_request_api, name="send request api"),

    path('api/friendRequest', view_friends_request_api, name="friendRequest api"),

    path('api/acceptRequest', accept_friend_request_api, name="acceptRequest api"),

    path('api/declineRequest', decline_friend_request_api, name="declineRequest api"),

    path('api/viewFriends', view_friends_api, name="viewFriends api"),

    path('api/removeFriends', remove_friend_api , name="removeFriend api"),

    path('api/profile/<int:profile_id>', profile_api, name="profile api"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)




