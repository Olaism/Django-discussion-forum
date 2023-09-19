from django.urls import resolve, reverse
from django.test import TestCase

from ..forms import NewTopicForm
from ..models import Board, Topic, Post
from ..views import home, board_topics, new_topic

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Example', description='All about testing')
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
        
class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='example', description='example test case')
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.response = self.client.get(url)
        
    def test_board_topics_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_view_resolve_correct_url(self):
        view = resolve(f'/boards/{self.board.pk}/')
        self.assertEquals(view.func, board_topics)
        
    def test_board_topics_contain_link_back_to_neccessary_page(self):
        home_url = reverse('home')
        new_topic_url = reverse("new_topic", args=(self.board.pk,))
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))
    
    
class NewTopicTests(TestCase):
    
    def setUp(self):
        self.board = Board.objects.create(name="Test", description='Test case')
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(url)
        
    def test_new_topic_view_successs_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_new_topic_view_not_found(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/{0}/new/'.format(self.board.pk))
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
        board_url = reverse('board_topics', args=(self.board.pk,))
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(board_url))


class NewTopicPostTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="test", description="test case")
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})

    def test_new_topic_valid_post_data(self):
        response = self.client.post(self.url, {'subject': 'Test title', 'message': 'Lorem ipsum dolor sit amet'})
        self.assertRedirects(self.response, reverse('board_topics', args=(self.board.pk,)))
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












