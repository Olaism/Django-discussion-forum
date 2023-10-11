from django.db import models
from django.urls import reverse

class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('board_topics', kwargs={'pk': self.pk})
    
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='topics')
    
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
        return self.message[:30]
    
    
    
    
    
    