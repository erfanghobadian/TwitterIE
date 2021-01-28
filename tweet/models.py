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

    hashtags = models.ManyToManyField(
        to='Hashtag',
        null=True
    )

    media = models.FileField(
        upload_to='media',
        null=True
    )

    def extract_hashtags(self):
        words = self.text.split()
        hashtags = []
        for word in words:
            if word[0] == '#':
                hashtags.append(word[1:])
        return hashtags

    def save(self, *args, **kwargs):
        is_created = not self.pk
        super(Tweet, self).save(*args, **kwargs)
        if is_created:
            for hashtag in self.extract_hashtags():
                obj, _ = Hashtag.objects.get_or_create(
                    tag=hashtag,
                )
                self.hashtags.add(obj)


class Like(BaseModel):
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE
    )

    tweet = models.ForeignKey(
        to=Tweet,
        on_delete=models.CASCADE,
    )


class Retweet(BaseModel):
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE
    )

    tweet = models.ForeignKey(
        to=Tweet,
        on_delete=models.CASCADE,
    )



class Hashtag(BaseModel):
    tag = models.CharField(
        max_length=255
    )
