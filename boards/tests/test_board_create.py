from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import BoardCreateView

User = get_user_model()

class BoardCreateTestCase(TestCase):
    
    def setUp(self):
        self.username = 'useradmin'
        self.password = 'adminpassword'
        user = User.objects.create_user(username=self.username, email='useradmin@gmail.com', password=self.password)
        user.is_staff = True
        user.save()
        self.url = reverse('board_create')

class LoginRequiredBoardCreateViewTests(TestCase):
    
    def test_redirection(self):
        url = reverse('board_create')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")
        
class NonStaffBoardCreateViewTests(TestCase):
    
    def setUp(self):
        User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(reverse('board_create'))

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 403)
    

class BoardCreateViewTests(BoardCreateTestCase):
    
    def setUp(self):
       super().setUp()
       self.client.login(username=self.username, password=self.password)
       self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_func(self):
        view = resolve('/boards/create/')
        self.assertEquals(view.func.view_class, BoardCreateView)

    def test_has_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_fields(self):
        self.assertContains(self.response, "<input", 3)
        self.assertContains(self.response, 'type="text"', 2)

class SuccessfulBoardCreateViewTests(BoardCreateTestCase):
    
    def setUp(self):
        pass

    def test_redirection(self):
        pass

    def test_board_creation(self):
        pass

class InvalidBoardCreateViewTests(BoardCreateTestCase):

    def setUp(self):
        pass

    def test_status_code(self):
        pass

    def test_form_errors(self):
        pass