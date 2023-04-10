from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models

# Create your models here.

class Profile(models.Model):
    '''
    This profile will have defaults empty when creating account, 
    so later you are advised to change it 
    '''

    profile_username = models.CharField(max_length=50)
    profile_image = models.ImageField(null=True, blank=True)
    profile_email = models.EmailField(max_length=254)
    profile_city = models.CharField(max_length=254)
    profile_DoB = models.DateField(null=True)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.profile_username,
            'image': self.profile_image.url if self.profile_image else None,
            'email': self.profile_email,
            'city': self.profile_city,
            'DoB': self.profile_DoB,
            'api': reverse('profile api', kwargs={'profile_id': self.id}),
        }

class User(AbstractUser):

    username = models.CharField(max_length=50, unique=True)
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def to_dict(self):
        return { 
            'id':self.id,
            'username':self.username, 
        }

class FriendList(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User,blank=True,related_name="friends")

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'friends': [
                friends.to_dict()
                for friends in self.friends.all()
            ],
        }

    def add_friend(self,userID):
        if not userID in self.friends.all():
             self.friends.add(userID)

class FriendsRequest(models.Model):

    sender = models.ForeignKey(User,on_delete= models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False,default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def to_dict(self):
        return {
            'id':self.id,
            'sender': self.sender.to_dict(),
            'receiver': self.receiver.to_dict(),
            'is_active': self.is_active,
            'timestamp': self.timestamp,
        }

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_List = FriendList.objects.get(user=self.sender)
            if sender_friend_List:
                sender_friend_List.add_friend(self.receiver)
                self.delete()

    def decline(self):
        self.delete()

    
class Hobby(models.Model):
    
    hobby_name = models.CharField(max_length=254)
    profiles = models.ManyToManyField(Profile)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.hobby_name,
        }

