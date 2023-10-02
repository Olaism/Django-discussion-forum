from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView


User = get_user_model()

class PasswordResetTests(TestCase):
    
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password/reset/')
        self.assertEquals(view.func.view_class, PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_forms(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    
    def setUp(self):
        email = 'testuser@gmail.com'
        User.objects.create_user(username="testuser", email=email, password="testpassword")
        url = reverse("password_reset")
        self.response = self.client.post(url, {'email': email})
        

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):

    def setUp(self):
        url = reverse("password_reset")
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))






