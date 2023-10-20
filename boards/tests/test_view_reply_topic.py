from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.test import TestCase

from ..forms import PostForm
from ..models import Board, Topic, Post
from ..views import reply_topic

User = get_user_model()


class ReplyTopicTestCase(TestCase):
    '''Base test case to be used in all `reply_topic` view tests'''

    def setUp(self):
        self.board = Board.objects.create(name="test board", description="a description for test board")
        self.username = "testuser"
        self.password = "testpassword"
        user = User.objects.create_user(username=self.username, email="", password=self.password)
        self.topic = Topic.objects.create(subject="all about django test", board=self.board, starter=user)
        Post.objects.create(message="my first post here", topic=self.topic, created_by=user)
        self.url = reverse("reply_topic", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk})
        
class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        
class ReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f"/boards/{self.board.pk}/topics/{self.topic.pk}/reply/")
        self.assertEqual(view.func, reply_topic)

    def test_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)        
        
class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {"message": "My reply on your post"})
        
    def test_redirection(self):
        post = Post.objects.last()
        url = reverse("topic_posts", kwargs={"pk": self.board.pk, "topic_pk": self.topic.pk})
        topic_posts_url = "{url}?page={page}#{id}".format(url=url, page=self.topic.get_page_count(), id=post.pk)
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_created(self):
        self.assertTrue(Post.objects.exists())

    def test_posts_count(self):
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyTopicTests(ReplyTopicTestCase):

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_post_creation(self):
        self.assertEquals(Post.objects.count(), 1)        
        
        
        
        
        
        