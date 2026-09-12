from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Author, Post, Comment

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.get_or_create(
                user=user,
                defaults={'name': user.username}
            )
            login(request, user)
            messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz!')
            return redirect('home')
        else:
            messages.error(request, 'Ro\'yxatdan o\'tishda xatolik yuz berdi')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Xush kelibsiz!')
            return redirect('home')
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz!')
    return redirect('home')

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            author, created = Author.objects.get_or_create(
                user=request.user,
                defaults={'name': request.user.username}
            )
            Post.objects.create(title=title, content=content, author=author)
            messages.success(request, 'Post muvaffaqiyatli yaratildi!')
            return redirect('home')
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni to\'ldiring')
    return render(request, 'core/create_post.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and request.user.is_authenticated:
            Comment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, 'Izoh qo\'shildi!')
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, 'Izoh qo\'shish uchun tizimga kiring')
    return render(request, 'core/post_detail.html', {'post': post, 'comments': comments})