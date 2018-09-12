from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('author/<name>', views.getauthor, name='author'),
    path('article/<int:id>', views.getsingle, name='single_post'),
    path('topic/<name>', views.getTopic, name='topic'),
    path('login', views.getLogin, name='login'),
    path('logout', views.getLogout, name='logout'),
    path('create', views.getCreate, name='create'),
    path('profile', views.getProfile, name='profile'),
    path('update/<int:id>', views.getUpdate, name='update'),
    path('delete/<int:id>', views.getDelete, name='delete'),
    path('register', views.getRegister, name='register'),
]
