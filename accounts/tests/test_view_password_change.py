from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.test import TestCase

User = get_user_model()

class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse("password_change")
        login_url = reverse("login")
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')



class PasswordChangeTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        url = reverse("password_change")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve("/password/change/")
        self.assertEquals(view.func.view_class, PasswordChangeView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        self.assertContains(self.response, "<input", 4)
        self.assertContains(self.response, 'type="password"', 3)


class SuccessfulPasswordChangeTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse("password_change")
        self.response = self.client.post(self.url, data={'old_password': 'testpassword', 'new_password1': 'newtest_password', 'new_password2': 'newtest_password'})

    def test_redirection(self):
        self.assertRedirects(self.response, reverse("password_change_done"))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtest_password"))

    def test_user_authentication(self):
        response = self.client.get(reverse("home"))
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)

class InvalidPasswordChangeTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@mail.com", password="testpassword")
        url = reverse("password_change")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.post(url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpassword"))
        
        
class LoginRequiredPasswordChangeDoneTests(TestCase):
    def test_redirection(self):
        url = reverse("password_change_done")
        login_url = reverse("login")
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')
        
        
class PasswordChangeDoneTests(TestCase):
    
    def setUp(self):
        url = reverse("password_change_done")
        User.objects.create_user(username="testuser", email="testuser@mail.com", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)
        
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_view_function(self):
        view = resolve("/password/change/done/")
        self.assertEquals(view.func.view_class, PasswordChangeDoneView)
        
        
        