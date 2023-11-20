from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from accounts import views as account_views

urlpatterns = [
    path('', RedirectView.as_view(url='/boards/'), name='home'),
    path('boards/', include('boards.urls')),
    path('api/', include('boards.api.urls')),
    path('accounts/signup/', account_views.signup, name='signup'),
    path('settings/account/', account_views.UserUpdateView.as_view(), name='my_account'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name="password_change.html"), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
    path('password/reset/', include([
        path('', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'), name='password_reset'),
        path('done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
        path('<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
        path('complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    ])),
    path('admin/', admin.site.urls),
]
