from django.contrib.auth.models import User
from rest_framework import serializers
from wave_proj.wave_scraper.models import Article, Task


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['url', 'id', 'title', 'author', 'category', 'content']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_id', 'status', 'started_at', 'completed_at']