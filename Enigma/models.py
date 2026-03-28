from django.db import models
from django.contrib.auth.models import User


# ===============================
# PROFILE MODEL
# ===============================

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


# ===============================
# EVENT MODEL
# ===============================

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()

    image = models.ImageField(
        upload_to="event_images/",
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hosted_events"
    )

    attendees = models.ManyToManyField(
        User,
        related_name="joined_events",
        blank=True
    )

    likes = models.ManyToManyField(
        User,
        related_name="liked_events",
        blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


# ===============================
# EVENT PHOTO MODEL (Gallery)
# ===============================

class EventPhoto(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="photos"
    )
    image = models.ImageField(upload_to="event_gallery/")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.event.title}"


# ===============================
# COMMENT MODEL
# ===============================

class Comment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"