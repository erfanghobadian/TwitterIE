from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, LoginSerializer, ActivitySerializer
from .models import User, Activity, Follow
from rest_framework import filters, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView


class UserIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        a = super().has_permission(request, view) or (view.action in ['list', 'retrieve'])
        print(a)
        return a


class LoginAPIView(ModelViewSet):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=200
        )


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.action != 'create':
            kwargs['exclude_fields'] = ('token',)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def follow(self, request, *args, **kwargs):
        user = self.get_object()
        if Follow.objects.filter(follower=request.user, followee=user).exists():
            Follow.objects.filter(follower=request.user, followee=user).delete()
            Activity.objects.create(
                user=request.user,
                text='User {} Followed User {}'.format(request.user.username, user.username)
            )
        else:
            Follow.objects.create(follower=request.user, followee=user)
            Activity.objects.create(
                user=request.user,
                text='User {} Unfollowed Tweet {}'.format(request.user.username, user.username)
            )
        return Response(
            "Tweet Liked Successfully",
            status=200
        )


class ProfileUpdateAPIView(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class ActivityListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-created')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context





