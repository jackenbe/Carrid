from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Quiz(models.Model):
    university = models.CharField(max_length=100, blank=True,null=True)
    field = models.CharField(max_length=100, blank=True,null=True)
    major = models.CharField(max_length=100, blank=True,null=True)
    year = models.IntegerField()

    def __str__(self):
        return self.major

class LinkedIn(models.Model):
    Post_Options = [
        ("project", "Project"),
        ("event", "Event"),
        ("job", "Job / Internship"),
        ("learning", "Learning / Course"),
        ("other", "Other"),
    ]

    has_experience = models.BooleanField(
        default=True,
        help_text="Check if you already have something to post about."
    )

    topic_type = models.CharField(
        max_length=20,
        choices=Post_Options,
        default="project"
    )

    description = models.TextField(
        blank=True,
        help_text="Describe the experience (if you have one)."
    )

    key_learnings = models.TextField(
        blank=True,
        help_text="What did you learn or accomplish?"
    )

    image = models.ImageField(
        upload_to="linkedin_images/",
        blank=True,
        null=True,
        help_text="Image to attach to this LinkedIn post."
    )


    draft_text = models.TextField(blank=True)

    def __str__(self):
        return f"LinkedIn #{self.id} ({self.topic_type})"
    
class LinkedInAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField()
    linkedin_member_urn = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} LinkedIn Account"
