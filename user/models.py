from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.db import models


class User(AbstractUser):
    pass


class Follow(BaseModel):
    follower = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='followees'
    )
    followee = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

