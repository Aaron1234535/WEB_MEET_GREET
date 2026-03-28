from django import forms
from .models import Event, Profile, EventPhoto, Comment


# ===============================
# EVENT FORM
# ===============================

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date', 'image']
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }


# ===============================
# PROFILE FORM
# ===============================

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio']


# ===============================
# EVENT PHOTO FORM
# ===============================

class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ['image']


# ===============================
# COMMENT FORM
# ===============================

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
