from django.urls import resolve, reverse
from django.views.generic import RedirectView
from django.test import TestCase

class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 302)
        
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, RedirectView)
        
    def test_home_view_redirect_to_board_home_view(self):
        self.assertRedirects(self.response, '/boards/')
    
    
    
    