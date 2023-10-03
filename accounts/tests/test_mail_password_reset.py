from django.core import mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


User = get_user_model()

class PasswordResetMailTests(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        self.response = self.client.post(reverse('password_reset'), {'email': 'testuser@mail.com'})
        self.email = mail.outbox[0]

    def test_mail_subject(self):
        self.assertEqual("[Django Boards] Please reset your password",self.email.subject)

    def test_mail_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('testuser', self.email.body)
        self.assertIn('testuser@mail.com', self.email.body)

    def test_mail_to(self):
        self.assertEqual(['testuser@mail.com'], self.email.to)
        
        
        
        
        
        