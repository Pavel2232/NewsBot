from asgiref.sync import sync_to_async
from django.db.models import F

from news.models import News, Comment


@sync_to_async
def get_all_news() -> list:
    return list(News.objects.all().order_by('-created_at'))


@sync_to_async
def get_all_me_news(id_user: int, is_admin: bool) -> list:
    if is_admin:
        return list(News.objects.all().order_by('-created_at'))
    return list(
        News.objects.filter(
            owner__telegram_id=id_user
        ).order_by(
            '-created_at'
        )
    )


@sync_to_async
def get_all_news_title() -> list:
    return list(News.objects.all().values_list('title', flat=True))


@sync_to_async
def get_all_comments_by_news(id_news: int) -> list:
    return list(
        Comment.objects.filter(
            news_id=id_news
        ).annotate(
            owner_name=F(
                'owner__username'
            )
        )
    )
