from django.contrib import admin
from django.urls import path, re_path

from accounts import views as account_views
from boards import views as board_views

urlpatterns = [
    re_path('^$', board_views.home, name='home'),
    path('accounts/signup/', account_views.signup, name='signup'),
    path('boards/<int:pk>/', board_views.board_topics, name='board_topics'),
    path('boards/<int:pk>/new/', board_views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),
]
