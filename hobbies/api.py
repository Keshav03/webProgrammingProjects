import json
import os
from django.contrib import auth
from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.db.models import Q
from base64 import b64decode
from PIL import Image
from io import BytesIO

from .models import FriendList, Hobby, User, Profile, FriendsRequest

def profiles_api(request):

    auth.get_user(request)

    profiles = []
    for profile in Profile.objects.all():
        profiles.append(profile.to_dict())

    all_Hobbies = []
    for profile in Profile.objects.all():
        all_hobbies_QS = profile.hobby_set.all()
        profile_Hobbies= []
        for hobby in all_hobbies_QS:
            profile_Hobbies.append(hobby.hobby_name)
        all_Hobbies.append(profile_Hobbies)
        
    for hobby, profile in zip(all_Hobbies, profiles):
        profile['hobbies'] = hobby

    filteredProfiles = []
    currentUserInfo = ""
    for profile in profiles:
        if profile['name'] != str(auth.get_user(request)):
            filteredProfiles.append(profile)
        else:
            currentUserInfo = profile
    
    return JsonResponse({
        'profiles': filteredProfiles,
        'hobbies': [name.to_dict() 
                    for name in Hobby.objects.all()],
        'loggedUser': currentUserInfo,
    })


def users_api(request):#
    userlist = []
    for user in User.objects.filter(~Q(id=request.user.id)):
        if not user.is_superuser:
            userlist.append(user.to_dict())

    return JsonResponse({
        'users': userlist
    })


def send_request_api(request):
    from_user = request.user
    if request.method == "POST" and from_user.is_authenticated:  
        friend_id = request.POST.get("receiverUserID")
        if friend_id:
            receiver =  User.objects.get(id=friend_id)  #User receiving the request
            
            try:
                friend_request = FriendsRequest.objects.filter(sender=from_user,receiver=receiver,is_active=True)
                isFriends = FriendList.objects.get(user=from_user)
                if friend_request:
                    return JsonResponse({"Request":"Friend Request Already Sent"})
                friend_request = FriendsRequest(sender=from_user,receiver=receiver)
                friend_request.save()
                return JsonResponse({"Request":"Friend Request Sent"})
            except FriendsRequest.DoesNotExist:
                friend_request = FriendsRequest(sender=from_user,receiver=receiver)
                friend_request.save()
                return JsonResponse({"Request":"Friend Request Sent"})

    return HttpResponseBadRequest("Invalid method")

def view_friends_request_api(request):
    user = request.user
    
    if user.is_authenticated:
        current_user = User.objects.get(id=user.id)
        if user == current_user:
            friend_requests = FriendsRequest.objects.filter(receiver=current_user,is_active=True)
            newList =[]
            for request in friend_requests:
                data = request.to_dict()
                newList.append(data)
            return JsonResponse({
                    "request":newList
            })
    return JsonResponse({"ID": "t"})


def accept_friend_request_api(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        friend_request_id = request.POST.get("requestID")
        if friend_request_id:
            friend_request = FriendsRequest.objects.get(id=friend_request_id)
           
            receiver = friend_request.receiver.username
            user = str(user)
            if receiver == user:
                friend_request.accept()  # invoke accept function from FriendRequest Models
                return JsonResponse({"Response" : "Friend Request Accepted"})
        else:
            return JsonResponse({"Response" : "Cant Accept friend request"})
    return HttpResponseBadRequest("Invalid method")

def decline_friend_request_api(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        friend_request_id = request.POST.get('requestID')
        friend_request = FriendsRequest.objects.get(id=friend_request_id)
        if friend_request != None:
            friend_request.decline()
            return JsonResponse({"Response" : "Request Declined"})
        else:
            return JsonResponse({"Response" : "Request Null"})
    return HttpResponseBadRequest("Invalid method")

def view_friends_api(request):
    user = request.user
    if user.is_authenticated:
        current_user = User.objects.get(id=user.id)
        
        if user == current_user:  
            friend_list = FriendList.objects.get(user=current_user)
            return JsonResponse({
                    "friends":[ 
                        friend.to_dict()
                        for friend in friend_list.friends.all()
                    ]
            })
    return JsonResponse({"ID": "t"})

def remove_friend_api(request):
    user = request.user
    if request.method == "DELETE" and user.is_authenticated:
        data = json.loads(request.body)
        user_id =  data["friendID"]
        if user_id:
            removee = User.objects.get(id=user_id)
            removeeFriendList = FriendList.objects.get(user=removee)
            if user in removeeFriendList.friends.all():
                removeeFriendList.friends.remove(user)

            own_friend_list = FriendList.objects.get(user=user)
            own_friend_list.friends.remove(removee)

            return JsonResponse({"Response" : "Friend Remove sucessfull"})
        else:
            return JsonResponse({"Response" : "User doesnt Exist"})
    return HttpResponseBadRequest("Invalid method")

def profile_api(request, profile_id):
    if request.method == "DELETE":
        body = json.loads(request.body)
        profile = get_object_or_404(Profile, id=profile_id)
        hobby = get_object_or_404(Hobby, hobby_name=body['hobbyToDelete'])
        hobby.profiles.remove(profile)
        hobby.save()
        return JsonResponse({})

    if request.method == "PUT":
        profile = get_object_or_404(Profile, id=profile_id)
        body = json.loads(request.body)
        email = body['email']
        city = body['city']
        dob = body['dob']
        hobby = body['hobby']
        image = body['image']
        print(image)
        if image != None:
            """ splitting done in order to fix "Incorrect padding" https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding """
            im = Image.open(BytesIO(b64decode(image.split(',')[1])))
            im.save('static\\profile_images\\' + profile.profile_username + 'profileImage.png')
            profile.profile_image = profile.profile_username + "profileImage.png";
        if hobby != "" :
            hobbies = hobby.capitalize()
            existing_hobby = get_object_or_404(Hobby, hobby_name = hobbies)
            existing_hobby.profiles.add(profile)
        profile.profile_email = email
        profile.profile_city = city
        profile.profile_DoB = dob
        profile.save()
        return JsonResponse({})

    if request.method == "POST":
        body = json.loads(request.body)
        profile = get_object_or_404(Profile, id=profile_id)
        hobby = body["hobby"]
        hobbies = hobby.capitalize()
        try:
            existing_hobby = get_object_or_404(Hobby, hobby_name=hobbies)
            return JsonResponse({})
        except:
            new_hobby=Hobby.objects.create(hobby_name=hobbies)
            new_hobby.save()
        return JsonResponse({})
    return HttpResponseBadRequest("Invalid method")
    
