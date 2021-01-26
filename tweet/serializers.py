from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'parent',
            'user',
            'text',
            'likes'
        ]

        extra_kwargs = {
            'user': {
                'required': False,
            }
        }

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def get_likes(self, instance):
        return {
            'count': instance.like_set.all().count(),
            'users': [UserSerializer(instance=like.user, exclude_fields=('token','email', 'first_name', 'last_name')).data for like in instance.like_set.all()]
        }
