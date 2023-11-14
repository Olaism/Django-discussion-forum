from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from ..models import Board, Topic, Post
from ..views import PostListView

User = get_user_model()

class TopicPostsViewTestCase(TestCase):
    
    def setUp(self):
        self.board = Board.objects.create(name="test", description="test for topic posts")
        user = User.objects.create_user(username="testuser", email="testuser@mail.com", password="testpassword")
        self.topic = Topic.objects.create(subject="test subject", board=self.board, starter=user)
        self.post = Post.objects.create(message="lorem ipsum dolor sit amet", topic=self.topic, created_by=user)
        self.url = reverse('topic_posts', kwargs={"slug": self.board.slug, 'topic_id': self.topic.id})
        self.edit_link = reverse('edit_post', kwargs={'slug': self.board.slug, 'topic_id': self.topic.id, 'post_id': self.post.id})


class TopicPostsTests(TopicPostsViewTestCase):
    
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f"/boards/{self.board.slug}/topics/{self.topic.id}/")
        self.assertEqual(view.func.view_class, PostListView)
        
    def test_view_contains_reply_link(self):
        reply_url = reverse('reply_topic', kwargs={'slug': self.board.slug, 'topic_id': self.topic.id})
        self.assertContains(self.response, reply_url)

    def test_view_contains_edit_link(self):
        User.objects.create_user(username='otheruser', email='otheruser@gmail.com', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, self.edit_link)

    def test_view_does_not_contain_edit_link_for_not_authenticated_user(self):
        self.assertNotContains(self.response, self.edit_link)
    
    
    
    
    
    