from django.contrib import admin
from django.urls import path, include
from .views import TweetViewSet


tweet_list = TweetViewSet.as_view(
    {'get': 'list',
     'post': 'create',
     }
)


tweet_detail = TweetViewSet.as_view(
    {'get': 'retrieve',
     'delete': 'destroy',
     }
)


tweet_like = TweetViewSet.as_view(
    {'post': 'like',
     }
)

tweet_retweet = TweetViewSet.as_view(
    {'post': 'retweet',
     }
)

urlpatterns = [
    path('', tweet_list),
    path('<int:pk>/', tweet_detail),
    path('<int:pk>/like', tweet_like),
    path('<int:pk>/retweet', tweet_retweet),
]
