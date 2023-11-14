from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Topic, Post
from ..views import PostUpdateView

User = get_user_model()


class PostUpdateViewTestCase(TestCase):
    '''
    Base test case to be used in all `PostUpdateView` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name="test board", description="all about the board test")
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, email="testuser@mail.com", password=self.password)
        self.topic = Topic.objects.create(subject="testing in django", board=self.board, starter=self.user)
        self.post = Post.objects.create(message="Hello, test!", topic=self.topic, created_by=self.user)
        self.url = reverse('edit_post', kwargs={
            'slug': self.board.slug,
            'topic_id': self.topic.id,
            'post_id': self.post.id
        })
        
class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    
    def test_redirection(self):
        '''
        Test if only logged in users can edit the posts
        '''
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        
        
class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        username = 'testuser02'
        password = 'testpassword02'
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)
        
    def test_status_code(self):
        '''
        A topic should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        '''
        self.assertEqual(self.response.status_code, 404)    
    
        
class PostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/boards/{self.board.pk}/topics/{self.topic.pk}/posts/{self.post.pk}/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<textarea', 1)     
        
class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'updated message'})
        
    def test_redirection(self):
        self.assertRedirects(self.response, reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_id': self.topic.id}))

    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'updated message')

class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)        
        
        
        
        