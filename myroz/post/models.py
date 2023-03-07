from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    # Поле для картинки (необязательное)
    image = models.ImageField(
        'Картинка',
        upload_to='post/',
        blank=True
    )
    # Аргумент upload_to указывает директорию,
    # в которую будут загружаться пользовательские файлы.
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comments', blank=True,
        null=True,)
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]

    def __str__(self):
        # выводим текст поста
        return self.text


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание сообщества")

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Комментировать запись'
    )

    created = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text


