import tempfile
import filecmp
import os

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User 
from django.db import IntegrityError

import datetime

from ..models import Show, UserDetails, Note

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


''' Image tests for models.note image files '''
class TestImageUpload(TestCase):

    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):

        user = User.objects.first()
        self.client.force_login(user)
        self.MEDIA_ROOT = tempfile.mkdtemp()

    ''' Create a temporary image file '''
    def create_temp_image_file(self):

        handle, tmp_img_file = tempfile.mkstemp(suffix='.jpg')
        img = Image.new('RGB', (10, 10) )
        img.save(tmp_img_file, format='JPEG')
        return tmp_img_file

    ''' Delete the associated image when deleting a note '''
    def test_delete_note_with_image_image_deleted(self):

        img_file_path = self.create_temp_image_file()
        with self.settings(MEDIA_ROOT=self.MEDIA_ROOT):

            with open(img_file_path, 'rb') as img_file:
                response = self.client.post(reverse('note_detail', kwargs={'note_pk': 1} ), {'photo': img_file }, follow=True)
                
                self.assertEqual(200, response.status_code)

                note_1 = Note.objects.get(pk=1)
                img_file_name = os.path.basename(img_file_path)
                
                uploaded_file_path = os.path.join(self.MEDIA_ROOT, 'user_images', img_file_name)

                note_1 = Note.objects.get(pk=1)
                note_1.delete()

                self.assertFalse(os.path.exists(uploaded_file_path))
