from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Group(models.Model):
    """Group for categorizing posts."""
    title = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True,
    )
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Post model."""
    text = models.TextField(
        'Текст поста',
        help_text='Текст нового поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Comments to the posts."""
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Текст нового комментария',
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Model for users following other users."""
    is_cleaned = False

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self) -> str:
        user_name = self.user.get_username()
        following_name = self.following.get_username()
        return f'{user_name} - {following_name}'

    def clean(self):
        """
        Raise ValidatioError if the user and the author are
        the same User instance.

        """
        self.is_cleaned = True
        if self.user == self.author:
            raise ValidationError(
                'Пользователь не может подписаться на самого себя'
            )
        super(Follow, self).clean()

    def save(self, *args, **kwargs):
        """
        Does not save an Follow instance if the user and the author are
        the same User instance.

        """
        if not self.is_cleaned:
            self.full_clean()
        super(Follow, self).save(*args, **kwargs)
