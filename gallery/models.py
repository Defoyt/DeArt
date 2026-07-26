from django.db import models
from django.contrib.auth.models import User


# 1. Модель Категорий (пейзажи, портреты, аниме и т.д.)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    def __str__(self):
        return self.name


# 2. Модель Фотографии
class Photo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='photos/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    # Связь с автором (кто выложил)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")

    # Лайки и Избранное (связь "многие ко многим")
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True, verbose_name="Лайки")
    favorites = models.ManyToManyField(User, related_name='favorite_photos', blank=True, verbose_name="В избранном")

    # Счётчик просмотров
    views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return self.title


# 3. Модель Комментариев
class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', verbose_name="Фотография")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.photo.title}"