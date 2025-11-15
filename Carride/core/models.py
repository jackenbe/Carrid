from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.
class Quiz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quiz', null=True, blank=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown'} - {self.major or 'No major'}"

class LinkedInPost(models.Model):
    """Stores LinkedIn post data with support for multiple images"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='linkedin_posts')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class LinkedInPostImage(models.Model):
    """Store multiple images for each LinkedIn post"""
    post = models.ForeignKey(LinkedInPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='linkedin_posts/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.post.id}"

    class Meta:
        ordering = ['uploaded_at']
    
class LinkedInAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(default=timezone.now)
    linkedin_member_urn = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} LinkedIn Account"
