from django.urls import path

from hobbies import views

from hobbies import  viewsets, api
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profiles', viewsets.ProfileViewSet)



app_name = 'hobbies'

urlpatterns = [
    
    path('', views.redirectLogin, name='redirectLogin'),
    # signup page
    path('signup/', views.signup, name='signup'),
    # login page
    path('login/', views.login, name='login'),
    # logout page
    path('logout/', views.logout, name='logout'),
    # members page  
    path('members/', views.members_view, name='members'),
    # profile page
    path('profile/', views.profile_view, name='profile'),
]
