from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username="AnyName")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="test-slug",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=("Тестовый пост, но определенно нужно,"
                  "что бы текст был длинее,"
                  "что бы проверить,"
                  "различные взаимодействия с ним")
        )
        cls.templates = [
            reverse("posts:index"),
            reverse("posts:posts", kwargs={"slug": cls.group.slug}),
            reverse("posts:profile", kwargs={"username": cls.post.author}),
            reverse("posts:post_detail", kwargs={"post_id": cls.post.id}),
        ]
        cls.templates_url_names = {
            reverse("posts:index"): "posts/index.html",
            reverse("posts:posts", kwargs={"slug": cls.group.slug}
                    ): "posts/group_list.html",
            reverse("posts:profile", kwargs={"username": cls.post.author}
                    ): "posts/profile.html",
            reverse("posts:post_detail", kwargs={"post_id": cls.post.id}
                    ): "posts/post_detail.html",
            reverse("posts:post_edit", kwargs={"post_id": cls.post.id}
                    ): "posts/create_post.html",
            reverse("posts:post_create"): "posts/create_post.html",
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_exists_at_desired_location(self):
        """URL-адреса доступны не авторизованному пользователю."""
        for adress in self.templates:
            with self.subTest(adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for url, template in self.templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_post_id_edit_url_exists_at_author(self):
        """Страница /posts/post_id/edit/ доступна автору."""
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous_on_auth_login(self):
        """Страница /create/ доступна авторизованному только пользователю."""
        response = self.guest_client.get("/create/", follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")
        response = self.authorized_client.get("/create/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_at_desired_location(self):
        """Страница /unexisting_page/ должна выдать ошибку."""
        response = self.guest_client.get("/unexisting_page/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
