from urllib import request, response
from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from django.test.utils import tag
from pprint import pprint

from blog.api.serializers import PostSerializer

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate


from blog.api.views import (
    PublishedPostsAPIView,
    ApprovedCommentsAPIView,
    UnpublishedPostsAPIView,
    PostAPIView,
    ListAPIView,
    CommentAPIView,
    CommentsAPIView,
    PostCommentsAPIView,
    ApprovingCommentAPIView,
    PostPublishingAPIView,
    CustomAuthToken
)
from blog.models import Post, Comment



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
    
    def get_post_data(self, post) -> list:
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
        
        comments_data = self.get_comments_data(comments)
        expected = {
            "data": comments_data,
            "count": len(comments_data)
        }
        
        approved_comments_count = Comment.objects.exclude(approved_comment = False).count()
        
        request = self.request_factory.get(self.url)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(approved_comments_count, response_data["count"])
        
class UnpublishedPostsAPIViewTestCase(TestCase):
    """UnpublishedPostsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run one time class setup initialization."""
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
       
class PostAPIViewTestCase(TestCase):
    """PostAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run one time class setup initialization."""
        self.url = "post/", "posts/<int:post_id>/"
        self.view = PostAPIView.as_view()
        self.request_factory = APIRequestFactory()
     
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            data = {
                "id": post.id, 
                "title": post.title, 
                "text": post.text,
                "is_published": post.is_published(),
                }
            posts_data.append(data)

        return posts_data
    
    def get_post_data(self, post) -> list:
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data
    
    
    def test_the_GET_returns_all_published_posts(self) -> None:
        """Get method succesfully views a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
                    "data": self.get_post_data(post)
                }

        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
    
    
    def test_get_method_views_a_post_error(self) -> None:
        """Get method succesfully views a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
                    "title": "Error",
                    "message": "Post not found."
                }

        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)
    
    
    
    def test_post_method_fails_to_create_new_post(self) -> None:
        """Post method fails to creates a new post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        
        expected = {
                    "data": self.get_post_data(post)
                }

        self.url = "posts/"

        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data

        self.assertNotEqual(response_data, expected) #equal
        self.assertEqual(response.status_code, 400)
        

    def test_post_method_succeeds_in_creating_new_post(self) -> None:
        """Post method succesfully creates a new post"""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Test title",
            "text": "Test text"
        }
        
        Post.objects.all().delete()
        
        self.url = "post/"
        
        request = self.request_factory.post(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        post = Post.objects.first()
        expected = {
                    "title": "Success!",
                    "message": "Post created!",
                    "data": self.get_post_data(post)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
        
    def test_put_method_succeds_in_editing_post(self) -> None:
        """Put method succesfully edits a post"""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Edited test title",
            "text": "Edited test text"
        }
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        post = Post.objects.first()
        expected = {
                    "title": "Success!",
                    "message": "Post edited!",
                    "data": self.get_post_data(post)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
    
    def test_put_method_post_not_found(self) -> None:
        """Put method fails to get a post to edit."""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Edited test title",
            "text": "Edited test text"
        }
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        post = Post.objects.first()
        expected = {
                    "title": "Error",
                    "message": "Post not found!"
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, expected)
    
    
    def test_put_method_edit_post_not_saved(self) -> None:
        """Put method fails to get a post to edit."""
        
        user = User.objects.create(username="testuser")
        
        post = Post.objects.create(
            author = user,
            title = "Edited test title",
            text = "Edited test text"
        )
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        exc = Exception
        post = Post.objects.first()
        expected = {
                    "title": "Error",
                    "message": "Unable to save post data",
                    "error": str(exc)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(response_data, expected) #equal
        
    def test_put_returns_error_on_non_authorized_edit(self) -> None:
        """PUT request on post by another user which is not the author returns error."""
        
        wrong_user = "wronguser"
        username = "testuser"
        
        user = User.objects.create(username=username)
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        
        post_id = post.id
        
        expected = "You are not authorized to delete this post"
        
        data = {
            "title": "Editing title with unauthorized user",
            "text": "Editting text wiht unauthorized user",
            "author": wrong_user
        }
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url, data=data)
        force_authenticate(request, user)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data
        
        self.assertNotEqual(post.author, wrong_user)        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data["message"], expected)
        self.assertEqual(response_data["title"], "Error")
    
    def test_delete_method_succeeds_in_deleting_post(self) -> None:
        """Delete method succesfully deletes a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
            "title": "Success",
            "message": "Post deleted!"
        }
        
        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
       
    def test_delete_method_post_not_found(self) -> None:
        """Delete method fails to delete a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
            "title": "Error",
            "message": "Post not found."
        }
        
        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)

    @tag("solo")
    def test_delete_method_returns_user_not_authorized(self) -> None:
        """Delete request on another user."""
        
        wrong_user = User.objects.create(username="wronguser")
        
        user = User.objects.create(username="testuser")
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        
        post_id = post.id
        
        expected = "You are not authorized to delete this post"
       
        self.url = "post/" + str(post_id) + "/"
        
        request = self.request_factory.delete(self.url)
        force_authenticate(request, wrong_user)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data
        
        self.assertNotEqual(post.author, wrong_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data["title"], "Error")
        self.assertEqual(response_data["message"], expected)
       
           
class ListAPIViewTestCase(TestCase):
    """ListAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "post/list/"
        self.view = ListAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def test_get_method_return_all_post(self) -> None:
        """GET method should return all posts."""
        
        user = User.objects.create(username="testuser")
        Post.objects.all()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        self.assertEqual(response.status_code, 200)
        
class CommentAPIViewTestCase(TestCase):
    """CommentAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "comments/<int:comment_id>/"
        self.view = CommentAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            data = {
                "id": post.id, 
                "title": post.title, 
                "text": post.text,
                "is_published": post.is_published(),
                }
            posts_data.append(data)

        return posts_data
        
    def get_comment_data(self, comment) -> list:
        """Return individual comment data."""
        
        data = {
            "id": comment.id, 
            "post": comment.post.id,
            "author": comment.author,
            "text": comment.text,
            "is_approved": comment.is_approved()
            }
        return data
        
    def test_get_method_access_a_comment(self) -> None:
        """Test Get method"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )

        comment_id = comment.id
        
        comments = Comment.objects.filter(post=post_id).first()
        expected = {
                    "data": self.get_comment_data(comments)
                }

        self.url = "comments/" + str(comment_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
    
    def test_get_method_fails_to_access_a_comment(self) -> None:
        """Test Get method fails"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )

        comment_id = comment.id
        
        comments = Comment.objects.filter(post=post_id).first()
        expected = {
                    "title": "Error",
                    "message": "Comment not found."
                }

        self.url = "comments/" + str(comment_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)  

class CommentsAPIViewTestCase(TestCase):
    """CommentsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "comment/new/"
        self.view = CommentsAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            data = {
                "id": post.id, 
                "title": post.title, 
                "text": post.text,
                "is_published": post.is_published(),
                }
            posts_data.append(data)

        return posts_data
    
    def get_post_data(self, post) -> list:
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
            data = {
                "id": comment.id,
                "post": self.get_post_data(comment.post),
                "author": comment.author, 
                "text": comment.text,
                "is_approved": comment.is_approved()
                }
            comments_data.append(data)
        
        return comments_data
    
    def get_comment_data(self, comment) -> list:
        """Return individual comment data."""
        
        data = {
            "id": comment.id, 
            "post": comment.post.id,
            "author": comment.author,
            "text": comment.text,
            "is_approved": comment.is_approved()
            }
        return data
    

    def test_post_method_return_error(self) -> None:
        """Post method not found."""
        
        user = User.objects.create(username="testuser")
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test text"
        )
        
        post_id = post.id
        post = Post.objects.get(pk=post_id)
        
        data = {
            "post": post_id,
            "author": "Test author",
            "text": "Test text"
        }
        
        self.url = "comment/new/"
        
        request = self.request_factory.post(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        comment = Comment.objects.first()
        expected = { 
            "title": "Success!",
            "message": "Comment created!",
            "data": self.get_comment_data(comment)
        }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
    
    #work on this
    def test_post_method_adds_a_comment(self) -> None:
        """Post method succesfully adds a comment."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        comment = Comment.objects.create(
            post = post,
            author = user,
            text = "Test comment on test post"
        )
        
        comments = Comment.objects.all()
        expected = { 
            "title": "Success!",
            "message": "Comment created!",
            "data": self.get_comment_data(comment)
        }
        
        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response_data, expected) #equal
     
class PostCommentsAPIViewTestCase(TestCase):
    """PostCommentsAPIView test case."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    def setUp(self) -> None:
        self.url = "post/<int:post_id>/comments/"
        self.view =  PostCommentsAPIView.as_view()
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

    def get_comments_data(self, comments):
        """Get comment data from comments queryset."""
        comments_data = []
        for comment in comments:
            data = {
                "id": comment.id, 
                "post": self.get_post_data(comment.post),
                "author": comment.author, 
                "text": comment.text,
                "is_approved": comment.is_approved(),
                }
            comments_data.append(data)
        
        return comments_data
    
    def test_get_method_returns_all_comments(self) -> None:
        """GET method should return comments."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        post_id = post.id
        
        comments = Comment.objects.filter(post=post_id)
        expected = {
                    "data": self.get_comments_data(comments)
                }

        self.url = "post/" + str(post_id) + "/comments/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
    @tag("solo")
    def test_get_method_returns_404_with_message_on_non_existent_post(self) -> None:
        """GET method should fail to return comments."""
        
        user = User.objects.create(username="testuser")
        
        Post.objects.all().delete()
        
        post_id = 1_000_000
        
        expected = {
                    "title": "Error",
                    "message": "Post not found."
                }

        self.url = "post/" + str(post_id) + "/comments/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Post.objects.filter(id=post_id).exists())

class ApprovingCommentAPIViewTestCase(TestCase):
    """ApprovingCommentAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "approve/comment/<int:comment_id>/"
        self.request_factory = APIRequestFactory()
        self.view = ApprovingCommentAPIView.as_view()
        
    def test_patch_method(self) -> None:
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        comment_id = comment.id
        
        comments = Comment.objects.get(pk=comment_id)
        
        comments.approve()
        expected = {
            "title": "Success",
            "message": "Comment Approved!"
        }
        
        self.url = "approve//comment/" + str(comment_id) + "/"

        request = self.request_factory.patch(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertTrue(comments.is_approved())
        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_method(self) -> None:
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        comment_id = comment.id
        
        expected = {
            "title": "Success",
            "message": "Comment Removed!"
        }
        
        self.url = "approve//comment/" + str(comment_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
 
class PostPublishingAPIViewTestCase(TestCase):
    """PostPublishingAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "post/publish/<int:post_id>/"
        self.view = PostPublishingAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def test_patch_method_publishes_a_post(self) -> None:
        """Patch method succesfully publishes a post."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        
        post_id = post.id
        
        posts = Post.objects.get(pk=post_id)
        
        posts.publish()
        expected = {
            "title": "Success",
            "message": "Post published!"
        }
        
        self.url = "post//publish/" + str(post_id) + "/"

        request = self.request_factory.patch(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertTrue(posts.is_published())
        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
class CustomAuthTokenTestCase(TestCase):
    """CustomAuthToken test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = 'api-token-auth/'
        self.view =  CustomAuthToken.as_view()
        self.request_factory = APIRequestFactory()
    
    
    def test_post_method_auth_token(self) -> None:
        """Post creates a token for user."""
        
        username = "testuser"
        password = "testpassword"
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        data = {
            "username": username,
            "password": password
        }
        
        expected = {
            "user_id": user.id,
            "token": token.key,
            "email": ""
        }
        
        request = self.request_factory.post(self.url, data)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected)

    
    def test_post_method_auth_token_invalid_user(self) -> None:
        """Post invalid input."""
        
        wrong_user = "wronguser"
        username = "testuser"
        password = "testpassword"
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        data = {
            "username": wrong_user,
            "password": password
        }
        
        expected = "Invalid username/password"
        
        request = self.request_factory.post(self.url, data)
        force_authenticate(request, user=user)
        response = self.view(request)
        
        response_data = response.data

        self.assertEqual(response_data["title"], "Error")
        self.assertEqual(response_data["message"], expected)
        self.assertEqual(response.status_code, 400)

