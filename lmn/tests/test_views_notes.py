
from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from django.contrib.auth.models import User




class TestDeleteNotes(TestCase):

    fixtures = ['test_notes', 'test_users']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_delete_notes(self):
        response = self.client.post(reverse('delete_notes', args=(2,)), follow=True)
        note_2 = Note.objects.filter(pk=2).first()
        self.assertIsNone(note_2)   # note is deleted

    def test_delete_someone_else_notes_not_auth(self):
        response = self.client.post(reverse('delete_notes',  args=(5,)), follow=True)
        self.assertEqual(403, response.status_code)
        note_5 = Note.objects.get(pk=5)
        self.assertIsNotNone(note_5)    # note still in database
