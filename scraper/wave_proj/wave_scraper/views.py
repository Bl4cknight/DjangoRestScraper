from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from wave_proj.wave_scraper.serializers import UserSerializer, ArticleSerializer, TaskSerializer
from wave_proj.wave_scraper.models import Article, Task
from wave_proj.wave_scraper.tasks import scraper
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'author']

    @action(detail=False, methods=['get'])
    def delete_all(self, request):
        Article.objects.all().delete()
        return Response('success')


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-started_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def delete_all(self, request):
        Task.objects.all().delete()
        return Response('success')


class ScraperView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pages': openapi.Schema(type=openapi.TYPE_INTEGER, description='number of pages to scrape'),
        }
    ),
        responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Response': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Scraper Async Task Started"
                )
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Response': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="Wrong Parameter"

                )
            }
        ),
    }
    )
    def post(self, request):
        pages = None
        if 'pages' in request.data:
            pages = request.data['pages']
        if pages and isinstance(pages, int):
            scraper.delay(pages)
            return Response({"Response": "Scraper Async Task Started"}, status=status.HTTP_200_OK)
        else:
            logger.error(pages)
            return Response({"Response": "Wrong Parameter"}, status=status.HTTP_400_BAD_REQUEST)
