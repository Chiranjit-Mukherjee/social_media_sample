# decorators.py

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def rate_limit(func):
    def wrapper(self, request, *args, **kwargs):
        user_id = str(request.user.id)
        cache_key = f'friend_request_count_{user_id}'
        count = cache.get(cache_key, 0)
        if count >= 3:
            response = {
                "error": "You have exceeded the maximum number of friend requests allowed"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        cache.set(cache_key, count + 1, timeout=60)  # Cache the count for 1 minute
        return func(self, request, *args, **kwargs)
    return wrapper

class CachedAPIView(APIView):
    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
