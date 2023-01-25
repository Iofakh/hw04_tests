from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
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

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post_model = PostModelTest.post
        group_model = PostModelTest.group
        expected_post_model_str = post_model.text[:15]
        expected_group_model_str = group_model.title
        self.assertEqual(expected_post_model_str, str(post_model))
        self.assertEqual(expected_group_model_str, str(group_model))
