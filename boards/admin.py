from django.contrib import admin

from .models import Board, Topic, Post

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'last_updated', 'board', 'starter', 'views')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'topic', 'created_at', 'created_by')