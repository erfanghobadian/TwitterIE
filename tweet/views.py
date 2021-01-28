from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Tweet, Like, Retweet
from user.models import Activity
from .serializers import TweetSerializer
from rest_framework import permissions, filters
from rest_framework.authentication import TokenAuthentication


class TweetIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or (view.action in ['list', 'retrieve'])


class TweetViewSet(ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created')
    serializer_class = TweetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [TweetIsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['hashtags__tag', 'text', 'user__username']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def like(self, request, *args, **kwargs):
        tweet = self.get_object()
        if Like.objects.filter(user=request.user, tweet=tweet).exists():
            Like.objects.filter(user=request.user, tweet=tweet).delete()
            Activity.objects.create(
                user=request.user,
                text='User {} Disliked Tweet {}'.format(request.user.username, tweet.text[:20])
            )
        else:
            Like.objects.create(user=request.user, tweet=tweet)
            Activity.objects.create(
                user=request.user,
                text='User {} Liked Tweet {}'.format(request.user.username, tweet.text[:20])
            )
        return Response(
            TweetSerializer(instance=tweet, context={'request': self.request}).data,
            status=200
        )




    def retweet(self, request, *args, **kwargs):
        tweet = self.get_object()
        if Retweet.objects.filter(user=request.user, tweet=tweet).exists():
            Retweet.objects.filter(user=request.user, tweet=tweet).delete()
            Activity.objects.create(
                user=request.user,
                text='User {} Retweeted Tweet {}'.format(request.user.username, tweet.text[:20])
            )
        else:
            Retweet.objects.create(user=request.user, tweet=tweet)
            Activity.objects.create(
                user=request.user,
                text='User {} UnRetweeted Tweet {}'.format(request.user.username, tweet.text[:20])
            )
        return Response(
            TweetSerializer(instance=tweet, context={'request': self.request}).data,
            status=200
        )
    
    def list(self, request, *args, **kwargs):
        return super(TweetViewSet, self).list(request, *args, **kwargs)


