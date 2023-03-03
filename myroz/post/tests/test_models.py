from .fixtures import PostFixturesTest


class PostModelTest(PostFixturesTest):
    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_object_post = post.text[:15]
        self.assertEqual(expected_object_post, str(post))
        self.assertEqual(expected_object_post, str(post))

    def test_object_name_is_title_field(self):
        """__str__  group - это строчка с содержимым group.title."""
        post = self.post
        expected_object_group = post.group.name
        self.assertEqual(expected_object_group, str(self.group.name))
