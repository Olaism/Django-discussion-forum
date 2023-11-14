from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..forms import NewTopicForm
from ..models import Board, Topic, Post
from ..views import new_topic

User = get_user_model()

class LoginRequiredNewTopicTests(TestCase):
    
    def test_redirection(self):
        board = Board.objects.create(name="tests", description="test description")
        url = reverse("new_topic", kwargs={'slug': board.slug})
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")
        
    
class NewTopicTests(TestCase):
    
    def setUp(self):
        self.board = Board.objects.create(name="Test", description='Test case')
        User.objects.create_user(username="testuser", email="testuser@mail.com", password="testpassword")
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        self.client.login(username="testuser", password="testpassword")
        self.response = self.client.get(url)
        
    def test_new_topic_view_successs_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_new_topic_view_not_found(self):
        url = reverse('new_topic', kwargs={'slug': 'slug-does-not-exists'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/{0}/new/'.format(self.board.slug))
        self.assertEqual(view.func, new_topic)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    def test_contains_appropiate_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
        
    def test_contains_neccessary_fields(self):
        self.assertContains(self.response, '<input type="text"')
        self.assertContains(self.response, "<textarea")
        self.assertContains(self.response, '<input type="submit"')

    def test_new_topic_contain_link_back_to_neccessary_page(self):
        home_url = reverse('home')
        board_url = reverse('board_topics', args=(self.board.slug,))
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(board_url))


class NewTopicPostTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="test", description="test case")
        self.url = reverse('new_topic', kwargs={'slug': self.board.slug})
        User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_new_topic_valid_post_data(self):
        response = self.client.post(self.url, {'subject': 'Test title', 'message': 'Lorem ipsum dolor sit amet'})
        topic = Topic.objects.last()
        self.assertRedirects(response, reverse('topic_posts', args=(self.board.slug, topic.pk)))
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        response = self.client.post(self.url, {'subject': '', 'message': ''})
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
