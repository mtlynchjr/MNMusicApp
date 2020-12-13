import tempfile
import filecmp
import os

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User 
from django.db import IntegrityError


import datetime

from ..models import Show, UserDetails

# Create your tests here.
import tempfile
import filecmp
import os 

from django.urls import reverse
from django.test import override_settings

from ..models import Note

from PIL import Image

# Create your tests here.

class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

class TestUserDetails(TestCase):
    
    fixtures = ['testing_users']

    def test_user_details_fails_without_user(self):
        userDetails = UserDetails(display_name='Display Name', location='Location', favorite_genres='Favorite, Genres, Here', bio='Bio')
        with self.assertRaises(IntegrityError):
            userDetails.save()

    def test_user_details_accepts_empty_values(self): #users do not add details immediately upon registering, therefore values can be null
        user = User.objects.get(pk=1)
        userDetails = UserDetails(user=user, display_name='', location='', favorite_genres='', bio='')
        userDetails.save()
