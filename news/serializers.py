from rest_framework import serializers

from news.models import News, Comment


class NewsCreateListSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class CommentCreateListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
