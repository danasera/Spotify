from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Song(models.Model):
    title = models.TextField()
    artist = models.TextField()
    image = models.ImageField()
    album = models.TextField()
    description = models.TextField("about")
    audio_file = models.FileField(blank=True, null=True)
    audio_link = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paginate_by = 2


    def __str__(self):
        return self.title


class Genre(models.Model):
    GENRES = (
        ('RAP', 'Рэп'),
        ('R&B', 'R&B'),
        ('CLASSIC', 'Классика'),
        ('JUZZ', 'Джаз'),
        ('ELECTRIC', 'ELECTRIC'),)
    genre = models.CharField(choices=GENRES, max_length=15, blank=True, null=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='genres')

    def __str__(self):
        return self.genre



class Rating(models.Model):
    song = models.ForeignKey(Song,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'song'), )
        index_together = (('user', 'song'), )


class Like(models.Model):
    song = models.ForeignKey(Song,
                               on_delete=models.CASCADE,
                               related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)


class Favourite(models.Model):
    song = models.ForeignKey(Song,
                               on_delete=models.CASCADE,
                               related_name='favourites')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    is_favourite = models.BooleanField(default=False)
