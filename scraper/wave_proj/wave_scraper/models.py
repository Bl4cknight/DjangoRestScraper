from djongo import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    content = models.TextField()
    objects = models.DjongoManager()


class Task(models.Model):
    task_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    objects = models.DjongoManager()
