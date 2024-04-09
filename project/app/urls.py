from django.urls import path
from app.views import SignUpView, UserSearchAPIView
from app.views import FriendRequestAPIView, FriendRequestDetailAPIView, FriendsListAPIView
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', obtain_auth_token, name='login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestAPIView.as_view(), name='friend-requests'),
    path('friend-requests/<int:pk>/', FriendRequestDetailAPIView.as_view(), name='friend-request-detail'),
    path('friends/', FriendsListAPIView.as_view(), name='friends-list'),
]