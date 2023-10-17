from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import Truncator

from markdown import markdown

class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('board_topics', kwargs={'pk': self.pk})
        
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').last()
    
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.pk} - {self.subject}"
        
    def get_absolute_url(self):
        return reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.pk})
    
    
class Post(models.Model):
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
    
    
    
    