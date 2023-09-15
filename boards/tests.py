from django.urls import resolve, reverse
from django.test import TestCase

from .models import Board
from .views import home, board_topics

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
        
    def test_board_topics_status_code(self):
        url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
    def test_board_topics_view_resolve_correct_url(self):
        view = resolve(f'/boards/{self.board.pk}/')
        self.assertEquals(view.func, board_topics)
        
    def test_board_topics_contain_link_back_to_homepage(self):
        pass
    
    
    
    