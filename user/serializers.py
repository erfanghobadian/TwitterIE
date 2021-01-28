from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from .models import User, Activity
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followees = serializers.SerializerMethodField()
    tweets = serializers.SerializerMethodField()

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
            'followees',
            'token',
            'tweets',
            'avatar'
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

    def update(self, instance, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password', None)
            if password:
                instance.set_password(raw_password=password)
                instance.save()
            return super(UserSerializer, self).update(instance, validated_data)

    def get_token(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        return token.key

    def get_followees(self, instance):
        return {
            'count': instance.followees.all().count(),
            'users': [UserSerializer(instance=follow.user, exclude_fields=(
            'token', 'email', 'first_name', 'last_name', 'followers')).data.update({'time': follow.created}) for follow
                      in instance.followees.all()]
        }

    def get_followers(self, instance):
        return {
            'count': instance.followers.all().count(),
            'users': [UserSerializer(instance=follow.user, exclude_fields=('token', 'email', 'first_name', 'last_name', 'followers')).data.update({'time': follow.created}) for follow in instance.followers.all()]
        }

    def get_tweets(self, instance):
        return list(instance.tweet_set.all().values_list('id', flat=True))


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise NotAuthenticated(
                'A user with this user and password is not found.'
            )
        return UserSerializer(instance=user).data

    def to_representation(self, instance):
        return instance


class ActivityListSerializer(serializers.ListSerializer):
    pass


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'created',
            'text',
        )






