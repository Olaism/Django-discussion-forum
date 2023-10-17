from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import SignupForm
from ..views import signup

User = get_user_model()

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    def test_views_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)
        
    def test_form_has_fields(self):
        form = SignupForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
        
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        
class SuccessfulSignupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {
            'username': 'Testuser',
            'email': 'testuser@mail.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        
    def test_redirection(self):
        self.assertRedirects(self.response, reverse('login'))

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
        
        
class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
        
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
        
        
        
        
        
        