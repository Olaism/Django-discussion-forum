import uuid
import math
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify, Truncator

from markdown import markdown

class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.SlugField(null=True, unique=True)
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('board_topics', kwargs={'slug': self.slug})
        
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').last()
    
class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.pk} - {self.subject}"
        
    def get_absolute_url(self):
        return reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_id': self.id})
        
    def get_page_count(self):
        count = self.posts.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)
        
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]
            
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey('auth.User',  null=True, on_delete=models.SET_NULL, related_name='+')
    
    def __str__(self):
        truncated_msg = Truncator(self.message)
        return truncated_msg.chars(30)
    
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
    
    
    
    