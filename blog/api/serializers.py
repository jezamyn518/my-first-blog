from blog.models import Post, Comment

from rest_framework.serializers import ModelSerializer


class PostSerializer(ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["id", "title", "text", "author",]

class CommentSerializer(ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ["id", "post",  "author", "text",]