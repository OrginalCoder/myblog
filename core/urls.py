from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-yaratish/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]