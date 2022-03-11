from django.conf import settings
from django.db import models
from django.utils import timezone
#from django.conf import settings
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from rest_framework.authtoken.models import Token


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def str(self):
        return self.title

    def is_published(self):
        """Check if post is published."""
        
        return self.published_date is not None


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def str(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def is_approved(self):
        """Check if the comment is approved."""
        return  self.approved_comment is not True

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#ef create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance)