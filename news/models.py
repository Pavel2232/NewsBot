from django.db import models
from django.db.models import Q


class BaseDateTime(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )


class TgUser(BaseDateTime):

    telegram_id = models.PositiveBigIntegerField(
        unique=True,
        verbose_name='Идентификатор Telegram'
    )

    username = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Имя пользователя'
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name='Является ли администратором'
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return f'{self.username if self.username else self.telegram_id}'


class News(BaseDateTime):
    owner = models.ForeignKey(
        TgUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец новости',
        related_name='news',
    )

    title = models.CharField(
        max_length=60,
        verbose_name='Заголовок статьи',
        unique=True,
    )

    text = models.TextField(
        max_length=4095,
        verbose_name='Текст статьи'
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'{self.title}'


class Like(BaseDateTime):
    owner = models.ForeignKey(
        TgUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец лайка',
        related_name='likes',
    )

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name='Владелец новости',
        related_name='likes',
    )

    like = models.BooleanField(
        default=True,
        verbose_name='Лайк'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'news'],
                condition=Q(like=True),
                name='unique_like'
            )
        ]

    def __str__(self):
        return f'{self.owner.telegram_id} {self.news.title}'


class Comment(BaseDateTime):
    owner = models.ForeignKey(
        TgUser,
        on_delete=models.CASCADE,
        verbose_name='Владелец лайка',
        related_name='comments',
    )

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        verbose_name='Владелец новости',
        related_name='comments',
    )

    text = models.TextField(
        max_length=4095,
        verbose_name='Текст комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.text}'
