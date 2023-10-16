from django.urls import resolve, reverse
from django.test import TestCase

from ..models import Board
from ..views import TopicListView

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
        self.assertEquals(view.func.view_class, TopicListView)
        
    def test_board_topics_contain_link_back_to_neccessary_page(self):
        home_url = reverse('home')
        new_topic_url = reverse("new_topic", args=(self.board.pk,))
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))