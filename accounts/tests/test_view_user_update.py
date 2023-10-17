from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import UserUpdateView

User = get_user_model()

class UserUpdateTestCase(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, email='testuser@gmail.com', password=self.password)
        self.user.first_name = 'test'
        self.user.last_name = 'user'
        self.user.save()
        self.url = reverse('my_account')

class LoginRequiredUserUpdateTests(UserUpdateTestCase):

    def test_redirection(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

class UserUpdateTests(UserUpdateTestCase):

    def setUp(self):
        super().setUp() 
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/settings/account/')
        self.assertEquals(view.func.view_class, UserUpdateView)

    def test_has_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulUserUpdateTests(UserUpdateTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'first_name': 'john', 'last_name': 'wick', 'email': 'johnwick@gmail.com'})

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_fields_values(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'john')
        self.assertEquals(self.user.last_name, 'wick')
        self.assertEquals(self.user.email, 'johnwick@gmail.com')

class InvalidUserUpdateTests(UserUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'email': 'invalid'})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_fields_values(self):
        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'test')
        self.assertEquals(self.user.last_name, 'user')
        self.assertEquals(self.user.email, 'testuser@gmail.com')
        
        
        
        