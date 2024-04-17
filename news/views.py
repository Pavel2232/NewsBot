from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from news.models import News, Comment
from news.serializers import NewsCreateListSerializers, CommentCreateListSerializers


class CreateNewsView(CreateAPIView):
    model = News
    serializer_class = NewsCreateListSerializers
    permission_classes = [IsAuthenticated, ]


class ListNewsView(CreateAPIView):
    model = News
    serializer_class = NewsCreateListSerializers


class DestroyNewsView(DestroyAPIView):
    model = News
    serializer_class = NewsCreateListSerializers


class CreateCommentsView(CreateAPIView):
    model = Comment
    serializer_class = CommentCreateListSerializers
    permission_classes = [IsAuthenticated, ]


class ListCommentsView(ListAPIView):
    model = Comment
    serializer_class = CommentCreateListSerializers


class DestroyCommentsView(CreateAPIView):
    model = Comment
    serializer_class = CommentCreateListSerializers
