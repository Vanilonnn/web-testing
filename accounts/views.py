from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
from .forms import TopicForm, CommentForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Получаем пользователя
            login(request, user)  # Логиним
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Пользователь уже существует!'})

        user = User(username=username)
        user.set_password(password)  # Хешируем и сохраняем пароль
        user.save()

        return redirect('login')  # После регистрации перенаправляем на вход

    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html')

# Главная страница форума (список тем)
def forum_home(request):
    topics = Topic.objects.all().order_by('-created_at')
    return render(request, 'forum/forum_home.html', {'topics': topics})

# Создание новой темы (только для авторизованных пользователей)
@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum_home')
    else:
        form = TopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})

# Страница темы с комментариями
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = topic.comments.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.topic = topic
            comment.author = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = CommentForm()
    return render(request, 'forum/topic_detail.html', {'topic': topic, 'comments': comments, 'form': form})