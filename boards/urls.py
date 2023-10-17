from django.urls import path, re_path, include

from boards import views as board_views


urlpatterns = [
    re_path('^$', board_views.BoardListView.as_view(), name='board_home'),
    path('create/', board_views.BoardCreateView.as_view(), name='board_create'),
    path('<int:pk>/', board_views.TopicListView.as_view(), name='board_topics'),
    path('<int:pk>/new/', board_views.new_topic, name='new_topic'),
    path('<int:pk>/topics/<int:topic_pk>/', board_views.PostListView.as_view(), name='topic_posts'),
    path('<int:pk>/topics/<int:topic_pk>/reply/', board_views.reply_topic, name="reply_topic"),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', board_views.PostUpdateView.as_view(), name='edit_post'),
]