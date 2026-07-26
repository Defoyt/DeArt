from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Photo, Category, Comment
from .forms import PhotoForm, CommentForm


# 1. Главная страница: список фото + поиск и фильтр по категориям
def photo_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    photos = Photo.objects.all().order_by('-created_at')

    if query:
        photos = photos.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        photos = photos.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'gallery/photo_list.html', {
        'photos': photos,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


# 2. Детальная страница фото + счётчик просмотров + комментарии
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    # Увеличиваем просмотры при каждом открытии
    photo.views_count += 1
    photo.save(update_fields=['views_count'])

    comments = photo.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = CommentForm()

    return render(request, 'gallery/photo_detail.html', {
        'photo': photo,
        'comments': comments,
        'form': form,
    })


# 3. Добавление фотографии (только для авторизованных)
@login_required
def photo_create(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'gallery/photo_form.html', {'form': form, 'title': 'Добавить фото'})


# 4. Редактирование фотографии (только автор)
@login_required
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'gallery/photo_form.html', {'form': form, 'title': 'Редактировать фото'})


# 5. Удаление фотографии (только автор)
@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk, author=request.user)
    if request.method == 'POST':
        photo.delete()
        return redirect('photo_list')
    return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})


# 6. Лайки
@login_required
def photo_like(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('photo_detail', pk=pk)


# 7. Избранное
@login_required
def photo_favorite(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.favorites.all():
        photo.favorites.remove(request.user)
    else:
        photo.favorites.add(request.user)
    return redirect('photo_detail', pk=pk)


# 8. Страница сохранённого в избранное
@login_required
def favorites_list(request):
    photos = request.user.favorite_photos.all().order_by('-created_at')
    return render(request, 'gallery/favorites.html', {'photos': photos})


# 9. Профиль пользователя (со счётчиком его работ)
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_photos = profile_user.photos.all().order_by('-created_at')
    return render(request, 'gallery/profile.html', {
        'profile_user': profile_user,
        'photos': user_photos,
        'photos_count': user_photos.count(),
    })


# 10. Регистрация, Вход, Выход
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = UserCreationForm()
    return render(request, 'gallery/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('photo_list')
    else:
        form = AuthenticationForm()
    return render(request, 'gallery/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('photo_list')