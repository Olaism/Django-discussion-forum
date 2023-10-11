from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from ..models import Board, Topic, Post
from ..views import topic_posts

User = get_user_model()


class TopicPostsTests(TestCase):
    
    def setUp(self):
        self.board = Board.objects.create(name="test", description="test for topic posts")
        user = User.objects.create_user(username="testuser", email="testuser@mail.com", password="testpassword")
        self.topic = Topic.objects.create(subject="test subject", board=self.board, starter=user)
        Post.objects.create(message="lorem ipsum dolor sit amet", topic=self.topic, created_by=user)
        url = reverse('topic_posts', kwargs={"pk": self.board.pk, 'topic_pk': self.topic.board.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f"/boards/{self.board.pk}/topics/{self.topic.pk}/")
        self.assertEqual(view.func, topic_posts)
        
    def test_view_contains_reply_link(self):
        pass

    def test_view_contains_edit_link(self):
        pass

    def test_view_does_not_contain_edit_link_for_unauthorized_user(self):
        pass
    
    
    
    
    
    