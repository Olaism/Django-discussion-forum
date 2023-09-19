from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from accounts import views as account_views
from boards import views as board_views

urlpatterns = [
    re_path('^$', board_views.home, name='home'),
    path('accounts/signup/', account_views.signup, name='signup'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('boards/<int:pk>/', board_views.board_topics, name='board_topics'),
    path('boards/<int:pk>/new/', board_views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),
]
