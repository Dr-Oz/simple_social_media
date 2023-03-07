from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from simple_social_media.myroz.post.models import Post
User = get_user_model()

class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса group/test-slug/
        Post.objects.create(
            id='post-id',
            text='Тестовый пост',
            author='username',
            group='test-slug',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_slug(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        """Страница /profile/<username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/username')
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        """Страница /post/<post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('/post/post-id')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        """Страница /post/<post_id>/edit доступна только автору."""
        response = self.guest_client.get('/post/post-id/edit')
        self.assertEqual(response.status_code, 200)


