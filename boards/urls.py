from django.urls import path, re_path, include

from boards import views as board_views


urlpatterns = [
    re_path('^$', board_views.BoardListView.as_view(), name='board_home'),
    path('create/', board_views.BoardCreateView.as_view(), name='board_create'),
    path('<slug:slug>/', board_views.TopicListView.as_view(), name='board_topics'),
    path('<slug:slug>/new/', board_views.new_topic, name='new_topic'),
    path('<slug:slug>/topics/<uuid:topic_id>/', board_views.PostListView.as_view(), name='topic_posts'),
    path('<slug:slug>/topics/<uuid:topic_id>/reply/', board_views.reply_topic, name="reply_topic"),
    path('<slug:slug>/topics/<uuid:topic_id>/posts/<uuid:post_id>/edit/', board_views.PostUpdateView.as_view(), name='edit_post'),
]