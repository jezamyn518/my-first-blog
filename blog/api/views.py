from blog.api.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class PostsDataMixin:
    """Mixin for getting posts data."""

    def get_posts_data(self, posts):
        """Get posts data from posts queryset."""
        
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
    
    
class CommentsDataMixin(PostsDataMixin):
    """Mixin for getting comment data."""
    
    def get_comments_data(self, comments):
        """Get comment data from comment queryset."""
        
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
    
    def get_comment_data(self, comment):
        """Return individual comment data."""
        
        data = {
            "id": comment.id, 
            "post": comment.post.id,
            "author": comment.author,
            "text": comment.text,
            "is_approved": comment.is_approved()
            }
        return data
            
    
class  PublishedPostsAPIView(PostsDataMixin, APIView):
    """Get all published posts."""
    
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """Get all published posts data."""
        
        posts = Post.objects.exclude(published_date=None)
        posts_data = self.get_posts_data(posts)
        response = {
            "data": posts_data, 
            "count": len(posts_data)
            }
        
        return Response(response, status=200)


class PostPublishingAPIView(APIView):
    """API for publishing posts."""
    
    def patch(self, request, post_id, *args, **kwargs):
        """Publishin a test."""
        
        post = Post.objects.get(pk=post_id)
        post.publish()
        response = {
            "title": "Success",
            "message": "Post published!"
            }
        return Response(response, status=200)


class UnpublishedPostsAPIView(PostsDataMixin, APIView):
    """API for unpublished posts."""

    def get(self, request, *args, **kwargs):
        """Get all published posts data."""
        
        posts = Post.objects.filter(published_date=None)
        posts_data = self.get_posts_data(posts)
        response = {
            "data": posts_data, 
            "count": len(posts_data)
            }
        
        return Response(response, status=200)


class PostAPIView(PostsDataMixin, APIView):
    """API for blog post."""

    def get(self, request, post_id, *args, **kwargs):
        """Get post data on given post id or primary key, pk."""
        
        try:
            post = Post.objects.get(pk=post_id)
            response = {
                "data": self.get_post_data(post)
            }
            return Response(response, 200)
        except Post.DoesNotExist:
            error_response = {
                "title": "Error",
                "message": "Post not found."
            }
            return Response(error_response, status=404)
        
    def post(self, request, *args, **kwargs):
        """Post the data given."""
        
        try:
            data = request.data
            serializer = PostSerializer(data=data)
            
            if serializer.is_valid():
                post = serializer.save()
                response = {
                    "title": "Success!",
                    "message": "Post created!",
                    "data": self.get_post_data(post)
                }
                
                return Response(response, status=201)
            else:
                raise ValueError(str(serializer.errors))
        except Exception as exc:
            error_response = {
                "title": "Error",
                "message": "Unable to save post data",
                "error": str(exc),
            }
            return Response(error_response, status=400)
        
    def put(self, request, post_id, *args, **kwargs):
        """Update blog post on given data with id"""
        
        try:
            data = request.data
            post = Post.objects.get(pk=post_id)
            serializer = PostSerializer(instance=post, data=data)
            
            if serializer.is_valid():
                post = serializer.save()
                response = {
                    "title": "Success!",
                    "message": "Post edited!",
                    "data": self.get_post_data(post)
                }
                
                return Response(response, status=201)
            else:
                raise ValueError(str(serializer.errors))
        except Post.DoesNotExist:
            error_response = {
                "title": "Error",
                "message": "Post not found!"
            }
            return Response(error_response, status=404)
        except Exception as exc:
            error_response = {
                "title": "Error",
                "message": "You are not authorized to delete this post",
                "error": str(exc)
            }
            return Response(error_response, status=403)

    def delete(self, request, post_id, *args, **kwargs):
        """Delete post in given post id or primary key, pk"""
        
        try:
            user = request.user
            
            post = Post.objects.get(pk=post_id)
            if user != post.author:
                error_response = {
                    "title": "Error",
                    "message": "You are not authorized to delete this post"
                }
                return Response(error_response, status=403)
            else:
                post.delete()
                response = {
                    "title": "Success",
                    "message": "Post deleted!"
                }
                return Response(response, status=200)
        except Post.DoesNotExist:
            error_response = {
                "title": "Error",
                "message": "Post not found."
            }
            return Response(error_response, status=404)

            
    

class ListAPIView(PostsDataMixin, APIView):
    """List all post data"""
    
    def get(self, request, format=None):
        """get method returns all post data wether published or not."""

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
   
class CommentAPIView(CommentsDataMixin, APIView):
    """API for accessing a comment."""
    
    def get(self, request, comment_id, *args, **kwargs):
        """Get comment data on given post id or primary key, pk"""
        
        try:
            comment = Comment.objects.get(pk=comment_id)
            response = {
                "data": self.get_comment_data(comment)
            }
            return Response(response, 200)
        except Comment.DoesNotExist:
            error_response = {
                "title": "Error",
                "message": "Comment not found."
            }
            return Response(error_response, status=404)


class CommentsAPIView(CommentsDataMixin, APIView):
    """API for posting comments."""
    
    def post(self, request, *args, **kwargs):
        """Posting a comment."""
    
        try:
            data = request.data
            serializer = CommentSerializer(data=data)
            
            if serializer.is_valid():
                comment = serializer.save()
                response = {
                    "title": "Success!",
                    "message": "Comment created!",
                    "data": self.get_comment_data(comment)
                }
                
                return Response(response, status=201)
            else:
                raise ValueError(str(serializer.errors))
        except Exception as exc:
            error_response = {
                "title": "Error",
                "message": "Unable to save comment data",
                "error": str(exc),
            }
            return Response(error_response, status=404)
        

class ApprovedCommentsAPIView(CommentsDataMixin, APIView):
    """API for getting the approved comments"""
    
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """Get all approved comment data."""
        
        comments = Comment.objects.exclude(approved_comment=False)
        comments_data = self.get_comments_data(comments)
        response = {
            "data": comments_data, 
            "count": len(comments_data)
            }
        
        return Response(response, status=200)
        

class ApprovingCommentAPIView(APIView):
    """API for approving comments."""
    
    def patch(self, request, comment_id, *args, **kwargs):
        """Approving comment with given comment id or primary key."""
        
        comment = Comment.objects.get(pk=comment_id)
        comment.approve()
        response = {
            "title": "Success",
            "message": "Comment Approved!"
            }
        return Response(response, status=200)
    
    def delete(self, request, comment_id, *args, **kwargs):
        """Removing comment."""
        
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        response = {
            "title": "Success",
            "message": "Comment Removed!"
            }
        return Response(response, status=200)
    
    
class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }
                return Response(response, 200)
            else:
                raise ValueError(str(serializer.errors))
        except Exception as exc:
            error_response = {
                "title": "Error",
                "message": "Invalid username/password",
                "error": str(exc)
            }
            return Response(error_response, status=400)
        

class PostCommentsAPIView(CommentsDataMixin, APIView):
    """API for getting comments for a specific post"""
    
    def get(self, request, post_id, *args, **kwargs):
        """Get post data on given post id or primary key, pk."""
        
        try:
            post_exists = Post.objects.filter(id=post_id).exists()
            if not post_exists:
                error_response = {
                "title": "Error",
                "message": "Post not found."
            }
                return Response(error_response, status=404)
            comment = Comment.objects.filter(post=post_id)
            response = {
                "data": self.get_comments_data(comment)
            }
            return Response(response, 200)
        except Exception as exc:
            error_response = {
                "title": "Error",
                "message": "Something went wrong, please contact administrator",
                "error": str(exc)
            }
            return Response(error_response, status=500)
            