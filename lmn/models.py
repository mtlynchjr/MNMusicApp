from django.db import models

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator

import datetime
from datetime import timedelta

from PIL import Image


# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False

""" A music artist """
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'Name: {self.name}'


""" A venue, that hosts shows. """
class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False) 

    def __str__(self):
        return f'Name: {self.name} Location: {self.city}, {self.state}'


""" A show - one artist playing at one venue at a particular date. """
class Show(models.Model):
    show_date = models.DateField(blank=False)
    show_time = models.TimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Artist: {self.artist} At Venue: {self.venue} On: {self.show_date} at {self.show_time}'


""" Displays details for user's note for a particular show """
""" User can post multiple notes for any one show """
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], blank=True, null=True)
    posted_date = models.DateTimeField(blank=False)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    """ Results displayed in readable string format for user """
    def __str__(self):
        photo_str = self.photo.url if self.photo else 'No photo.'
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Posted on: {self.posted_date}/nPhoto: {photo_str}'

    """ Saves photo to database. Save overrides any existing photo associated with note """
    def save(self, *args, **kwargs):
        existing_photo = Note.objects.filter(pk=self.pk).first()
        if existing_photo and existing_photo.photo:
            if existing_photo != self.photo:
                self.delete_photo(existing_photo.photo)

        super().save(*args, **kwargs)

    """ Removes photo from note """
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)

    """ Deletes image file entirely """
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)


""" Details on user """
class UserDetails(models.Model):
    user = models.OneToOneField('auth.User', blank=False, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=30, null=True)
    favorite_genres = models.TextField(max_length=150, null=True)
    bio = models.TextField(max_length=300, null=True)

    def __str__(self):
        return f'User: {self.user}; Display name: {self.display_name}; Location: {self.location}; Favorite genres: {self.favorite_genres}; Bio: {self.bio}'
