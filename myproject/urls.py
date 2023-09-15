from django.contrib import admin
from django.urls import path, re_path

from boards import views

urlpatterns = [
    re_path('^$', views.home, name='home'),
    path('boards/<int:pk>/', views.board_topics, name='board_topics'),
    path('admin/', admin.site.urls),
]
