from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Tweet, Like, Retweet


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    hasLiked = serializers.SerializerMethodField()
    hasRetweeted = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    replies2 = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'created',
            'user',
            'text',
            'likes',
            'hasLiked',
            'hasRetweeted',
            'parent',
            'replies',
            'replies2',

        ]

        extra_kwargs = {
            'user': {
                'required': False,
            }
        }


    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(TweetSerializer, self).__init__(*args, **kwargs)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)

    def create(self, validated_data):
        return super().create(validated_data)

    def get_likes(self, instance):
        return {
            'count': instance.like_set.all().count(),
            'users': [UserSerializer(instance=like.user, exclude_fields=(
            'token', 'email', 'first_name', 'last_name', 'followers', 'followees')).data for like in
                      instance.like_set.all()]
        }

    def get_hasLiked(self, instance):
        try:
            user = self.context['request'].user
            return Like.objects.filter(user=user, tweet=instance).exists()
        except:
            return False


    def get_hasRetweeted(self, instance):
        try:
            user = self.context['request'].user
            return Retweet.objects.filter(user=user, tweet=instance).exists()
        except:
            return False

    def get_user(self, instance):
        return UserSerializer(instance=instance.user, exclude_fields=(
            'token', 'email', 'followers', 'followees')).data


    def get_replies(self, instance):
        return list(Tweet.objects.filter(parent=instance).values_list('id', flat=True))

    def get_replies2(self, instance):
        return TweetSerializer(Tweet.objects.filter(parent=instance), many=True,  exclude_fields=('parent', )).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.parent:
            data['parent'] = instance.parent.id
        else:
            data['parent'] = None
        return data
