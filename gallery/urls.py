from django.urls import path
from . import views

urlpatterns = [
    # Главная и детальная
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),

    # Действия с фото (CRUD)
    path('photo/add/', views.photo_create, name='photo_create'),
    path('photo/<int:pk>/edit/', views.photo_edit, name='photo_edit'),
    path('photo/<int:pk>/delete/', views.photo_delete, name='photo_delete'),

    # Интерактив (лайки, избранное)
    path('photo/<int:pk>/like/', views.photo_like, name='photo_like'),
    path('photo/<int:pk>/favorite/', views.photo_favorite, name='photo_favorite'),

    # Страницы пользователя
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]