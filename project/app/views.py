# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from app.serializers import UserSerializer, UserSearchSerializer, FriendRequestSerializer, UsersSerializer
from app.models import FriendRequest
from app.decorators import rate_limit, CachedAPIView
from rest_framework.permissions import IsAuthenticated 



class SignUpView(APIView):
    """
    Documentation Here
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchAPIView(APIView, PageNumberPagination):
    """
    Documentation Here
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.page_size = 10

        serializer = UserSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            search_query = serializer.validated_data['search_query']
            users = User.objects.filter(email__icontains=search_query) |\
                    User.objects.filter(first_name__icontains=search_query) |\
                    User.objects.filter(last_name__icontains=search_query)

            page = self.paginate_queryset(users, request)
            serialized_users = UsersSerializer(page, many=True)
            return self.get_paginated_response(serialized_users.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FriendRequestAPIView(CachedAPIView):
    """
    Documentation Here
    """
    permission_classes = (IsAuthenticated,)

    @rate_limit
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the user has already sent more than 3 friend requests within the last minute
            # Implement rate limiting logic here
            friend_request = serializer.save()
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        friend_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data)


class FriendRequestDetailAPIView(APIView):
    """
    Documentation Here
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        friend_request = FriendRequest.objects.get(pk=pk)
        friend_request.accepted = True
        friend_request.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        friend_request = FriendRequest.objects.get(pk=pk)
        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendsListAPIView(APIView):
    def get(self, request):
        # Retrieve the list of friends for the current user
        friends = User.objects.filter(received_friend_requests__from_user=request.user, received_friend_requests__accepted=True) |\
                  User.objects.filter(sent_friend_requests__to_user=request.user, sent_friend_requests__accepted=True)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)