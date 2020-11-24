from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import datetime

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
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} On: {self.show_date}'


""" One user's opinion of one show. """
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} Text: {self.text} Posted on: {self.posted_date}'

""" Photo Class provides the user with the option of adding artist/show/venue photos. """
class Photo(models.Model):
    # Photos are encouraged, but optional and so requirements set to blank and null. Except user.
    user = models.ForeignKey('auth.User' , null=False , on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist , blank=True , null=True , on_delete=models.CASCADE)
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue , blank=True , null=True , on_delete=models.CASCADE)
    date_taken = models.DateTimeField(blank=True , null=True)
    # Creates destination directory "user_images" for photos.
    photo = models.ImageField(upload_to="user_images/" , blank=True , null=True)

    # Determines if user will see photos or "no photos" response.
    def __str__(self):
        # Displays message to user if no photos yet exist.
        photo_str = self.photo.url if self.photo else "No photos found. Add some!"
        # Displays photos to user with user-friendly informational string.
        return f"{self.user}'s photos of {self.artist} performing thie show {self.show} live at {self.venue} on {self.date_taken}\n{photo_str}"
