from django.db import transaction
from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'followers',
            'followees'
            'token',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                email=validated_data['email'],
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()

            return user

    def get_token(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        return token.key


