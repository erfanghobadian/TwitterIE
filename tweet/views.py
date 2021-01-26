from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Tweet, Like
from .serializers import TweetSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class TweetIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or (view.action in ['list', 'retrieve'])


class TweetViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [TweetIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def like(self, request, *args, **kwargs):
        tweet = self.get_object()
        Like.objects.get_or_create(user=request.user, tweet=tweet)
        return Response(
            "Tweet Liked Successfully",
            status=200
        )


