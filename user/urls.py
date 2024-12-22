from django.urls import path
from .views import UserSignUpView, UserSignInView, UserLogoutView, profile_view


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signin/', UserSignInView.as_view(), name='signin'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
]