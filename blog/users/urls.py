from django.urls import path
from .views import RegisterUser,UserPofile,PasswordCharged 

urlpatterns = [
    path("register/", RegisterUser.as_view(),name="Register"),
    path("profile/", UserPofile.as_view(),name="profile"),
    path("changePassword/", PasswordCharged.as_view(),name="ChangePassword")
    
]