from django.db import models
from core.models import BaseModel


class Tweet(BaseModel):
    parent = models.ForeignKey(
        to='Tweet',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE
    )

    text = models.TextField()


class Like(BaseModel):
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE
    )

    tweet = models.ForeignKey(
        to=Tweet,
        on_delete=models.CASCADE,
    )
