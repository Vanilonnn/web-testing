from django.contrib import admin
from django.urls import path, include

from accounts import views
from accounts.views import forum_home, create_topic, topic_detail, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home, name='home'),
    path('forum/', forum_home, name='forum_home'),
    path('forum/topic/new/', create_topic, name='create_topic'),
    path('forum/topic/<int:topic_id>/', topic_detail, name='topic_detail'),
]
