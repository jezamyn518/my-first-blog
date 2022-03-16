from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory

from blog.api.views import PublishedPostsAPIView
from blog.models import Post
class PublishedPostsAPIViewTestCase(APITestCase):
    """PublishedPostsAPIView test case."""

    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()

    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "post/published/"
        self.view = PublishedPostsAPIView.as_view()
        self.request_factory = APIRequestFactory()

    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            if post.is_published():
                data = {
                    "id": post.id, 
                    "title": post.title, 
                    "text": post.text,
                    "is_published": post.is_published(),
                    }
                posts_data.append(data)

        return posts_data

    def test_get_method_returns_all_published_post(self) -> None:
        """GET method should return all published post."""

        posts = Post.objects.all()

        user = User.objects.create(username="testuser")
        published_post = Post.objects.create(
            author = user,
            title="Test unpublished post",
            text="Test",
            published_date=timezone.now()
        )

        unpublished_post = Post.objects.create(
            author = user,
            title="Test unpublished post",
            text="Test",
            published_date=None
        )

        posts_data = self.get_posts_data(posts)
        expected = {
            "data": posts_data,
            "count": len(posts_data)
        }

        published_posts_count = Post.objects.exclude(published_date=None).count()
        

        request = self.request_factory.get(self.url)
        response = self.view(request)

        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(published_posts_count, response_data["count"])