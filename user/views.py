from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from .models import User
from rest_framework import filters


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response(
                {'error': 'Please provide both username and password'},
                status=HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        serializer = UserSerializer(
            instance=user
        )
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
        return serializer_class(*args, **kwargs)

