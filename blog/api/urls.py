from django.urls import path
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



urlpatterns = [
    path("post/list/", ListAPIView.as_view()),
    path("post/published/", PublishedPostsAPIView.as_view()),
    path("post/publish/<int:post_id>/", PostPublishingAPIView.as_view()), #publishing post
    path("post/unpublished/", UnpublishedPostsAPIView.as_view()),
    path("posts/", PostAPIView.as_view()), #creating post
    path("posts/<int:pk>/", PostAPIView.as_view()), #reading, updating and deleting posts
    path("comments/<int:comment_id>/", CommentAPIView.as_view()), #accessing comment
    path("comment/new/", CommentsAPIView.as_view()), #creating comment
    path("approve/comment/<int:comment_id>/", ApprovingCommentAPIView.as_view()), #approving comment
    path("comments/approved/", ApprovedCommentsAPIView.as_view()), #reading comment
    path('api-token-auth/', CustomAuthToken.as_view()),#Adding token for the user
    path('post/<int:post_id>/comments/', PostCommentsAPIView.as_view())

]