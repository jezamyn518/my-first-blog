from unittest import expectedFailure
from webbrowser import get
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.test import TestCase
from blog.api.serializers import PostSerializer
from blog.api.views import (
     PublishedPostsAPIView, 
    PostPublishingAPIView, 
    UnpublishedPostsAPIView, 
    PostAPIView, 
    ListAPIView, 
    CommentAPIView,
    CommentsAPIView,
     ApprovedCommentsAPIView,
    ApprovingCommentAPIView,
    CustomAuthToken,
    PostCommentsAPIView

    )
from blog.models import Post
from blog.models import Comment 

class PublishedPostsAPIViewTestCase(TestCase):

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


class UnpublishedPostsAPIViewTestCase(TestCase):
    """UnpublishedPostsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "post/unpublished/"
        self.view = UnpublishedPostsAPIView.as_view()
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
    
    def test_get_method_returns_all_unpublished_post(self) -> None:
        """Get method should return all unpublished post."""
        
        posts = Post.objects.all()
        
        user = User.objects.create(username="testuser")
        
        posts_data = self.get_posts_data(posts)
        expected = {
            "data": posts_data,
            "count": len(posts_data)
        }
        
        unpublished_posts_count = Post.objects.filter(published_date = None).count()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(unpublished_posts_count, response_data["count"])

class ListAPIViewTestCase(TestCase):
    """ListAPIview test case"""

    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "post/list/"
        self.view = ListAPIView.as_view()
        self.request_factory = APIRequestFactory()

    def PostSerializer(self, Post) -> None:
        """get the postserializer"""

        PostSerializer = []
        for serializer in PostSerializer:
            if serializer.is_published():
                data = {
                    "id": serializer.id, 
                    "title": serializer.title, 
                    "text": serializer.text,
                    "author": serializer.author,
                    "is_published": serializer.is_published(),
                    }
                PostSerializer.append(data)

        return PostSerializer

    def test_get_method_returns_all_List_post(self) -> None:
        """Get method should return all List post."""

        posts = Post.objects.all()

        user = User.objects.create(username="testuser")
        
        serializer = self.PostSerializer(posts)
        expected = {
            
        }
        
        
        List_posts_count = Post.objects.filter(published_date = None).count()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        serializer = self.view(request)
        
        response_data = serializer.data
        
        self.assertEqual(response_data, expected, 1)
        self.assertEqual(List_posts_count, response_data["count"])





class ApprovedCommentsAPIViewTestCase(TestCase):
    """ApprovedCommentsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "comments/approved/"
        self.view = ApprovedCommentsAPIView.as_view()
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
    
    def get_post_data(self, post):
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data
    
            
    def get_comments_data(self, comments) -> list:
        """Get comments data."""
        
        comments_data = []
        for comment in comments:
            if comment.is_approved():    
                data = {
                    "id": comment.id,
                    "post": self.get_post_data(comment.post),
                    "author": comment.author, 
                    "text": comment.text,
                    "is_approved": comment.is_approved()
                    }
                comments_data.append(data)
        
        return comments_data
    
    def test_get_method_returns_all_approved_post(self) -> None:
        """GET method should return all approved comments."""
        
        comments = Comment.objects.all()
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title="Test post",
                text="Test",
                )
        
        approved_comment = Comment.objects.create(
            author = "Test author",
            post = post,
            text = "Test approved comment",
            approved_comment = True
            )
        
        unapproved_comment = Comment.objects.create(
            author = "Test author",
            post = post,
            text = "Test unapproved comment",
            approved_comment = False
        )
        
        comments_data = self.get_comments_data(comments)
        expected = {
            "data": comments_data,
            "count": len(comments_data)
        }
        
        approved_comments_count = Comment.objects.exclude(approved_comment = False).count()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(approved_comments_count, response_data["count"])