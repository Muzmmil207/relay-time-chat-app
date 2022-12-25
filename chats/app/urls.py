from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

urlpatterns = [
    path("", views.users, name='home'),
    path("chat/<str:username>", views.chat, name='chat'),
    path('send/', views.send_direct, name="send-directs"),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='register/login.html',
            form_class=UserLoginForm
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),
    path('register/', views.register, name="register"),
]
