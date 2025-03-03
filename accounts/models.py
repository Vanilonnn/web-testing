from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=200, unique=True)  # Заголовок темы
    content = models.TextField()  # Описание темы
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор темы
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="comments")  # Связь с темой
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    content = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата публикации

    def __str__(self):
        return f"Комментарий от {self.author} в {self.topic.title}"
