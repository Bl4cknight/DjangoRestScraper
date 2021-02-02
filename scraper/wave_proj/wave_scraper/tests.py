import json
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from wave_proj.wave_scraper.models import Article, Task


class ArticleTestCase(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_list_articles(self):
        response = self.client.get('/articles/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_filter_articles(self):
        test_article = Article()
        test_article.category = 'adventure'
        test_article.author = 'pippo'
        test_article.save()
        response = self.client.get('/articles/?category=adventure&author=pippo', format='json')
        result = json.loads(response.content)['results'][0]
        self.assertEqual(result['category'], 'adventure')
        self.assertEqual(result['author'], 'pippo')

    def test_create_Article(self):
        response = self.client.post('/articles/', {
            "title": "test title",
            "author": "test author",
            "category": "test category",
            "content": "test content"
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_Article(self):
        test_article = Article()
        test_article.id = 1
        test_article.save()
        response = self.client.put('/articles/1/', {
            "title": "test title",
            "author": "test author",
            "category": "test category",
            "content": "test content"
        }, format='json')
        updated_article = Article.objects.get(id=1)
        self.assertEqual(updated_article.title, "test title")
        self.assertEqual(updated_article.author, "test author")
        self.assertEqual(updated_article.category, "test category")
        self.assertEqual(updated_article.content, "test content")

    def test_delete_article(self):
        test_article = Article()
        test_article.id = 1
        test_article.save()
        response = self.client.delete('/articles/1/', format='json')
        self.assertEqual(response.status_code, 204)


class TaskTestCase(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_list_tasks(self):
        response = self.client.get('/tasks/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_create_Task(self):
        response = self.client.post('/tasks/', {
            "id": 1,
            "task_id": "cf2be649-d616-43b2-a8e6-076d1ae2e44e",
            "status": "SUCCESS",
            "started_at": datetime.now(),
            "completed_at": datetime.now() + timedelta(minutes=5)
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_delete_article(self):
        test_task = Task()
        test_task.id = 1
        test_task.save()
        response = self.client.delete('/tasks/1/', format='json')
        self.assertEqual(response.status_code, 204)


class ScraperTestCase(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_scraper(self):
        response = self.client.post('/scraper/', {"pages": 1}, format='json')
        self.assertEqual(response.status_code, 200)
