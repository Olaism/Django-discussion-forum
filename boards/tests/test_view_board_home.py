from django.urls import resolve, reverse
from django.test import TestCase

from ..models import Board
from ..views import BoardListView

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Example', description='All about testing')
        url = reverse('board_home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func.view_class, BoardListView)
        
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'slug': self.board.slug})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))