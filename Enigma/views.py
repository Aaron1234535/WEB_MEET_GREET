from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .models import Event, Profile, EventPhoto, Comment
from .forms import EventForm, EventPhotoForm, ProfileForm, CommentForm


# ===============================
# HOME (Public)
# ===============================

def home(request):
    events = Event.objects.all().order_by("event_date")
    return render(request, "home.html", {"events": events})


# ===============================
# DASHBOARD (Private)
# ===============================

@login_required
def dashboard(request):
    events = Event.objects.all().order_by("event_date")
    return render(request, "dashboard.html", {"events": events})


# ===============================
# SIGNUP
# ===============================

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


# ===============================
# EVENT LIST
# ===============================

@login_required
def event_list(request):
    events = Event.objects.all().order_by("event_date")
    return render(request, "event_list.html", {"events": events})


# ===============================
# CREATE EVENT
# ===============================

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("dashboard")
    else:
        form = EventForm()

    return render(request, "create_event.html", {"form": form})


# ===============================
# EVENT DETAIL (Likes + Comments)
# ===============================

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Handle comment submission
    if request.method == "POST" and "comment_submit" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added!")
            return redirect("event_detail", event_id=event.id)
    else:
        comment_form = CommentForm()

    photos = event.photos.all()
    comments = event.comments.all().order_by("-created_at")

    return render(request, "event_detail.html", {
        "event": event,
        "photos": photos,
        "comment_form": comment_form,
        "comments": comments
    })


# ===============================
# LIKE EVENT
# ===============================

@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.likes.all():
        event.likes.remove(request.user)
    else:
        event.likes.add(request.user)

    return redirect("event_detail", event_id=event.id)


# ===============================
# RSVP TO EVENT
# ===============================

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
        messages.info(request, "You have canceled your RSVP.")
    else:
        event.attendees.add(request.user)
        messages.success(request, "You have successfully RSVPed!")

    return redirect("event_detail", event_id=event.id)


# ===============================
# UPLOAD EVENT PHOTO
# ===============================

@login_required
def upload_event_photo(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.event = event
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, "Photo uploaded successfully!")

    return redirect("event_detail", event_id=event.id)


# ===============================
# MY EVENTS
# ===============================

@login_required
def my_events(request):
    hosted_events = Event.objects.filter(
        created_by=request.user
    ).order_by("event_date")

    joined_events = request.user.joined_events.all().order_by("event_date")

    return render(request, "my_events.html", {
        "hosted_events": hosted_events,
        "joined_events": joined_events
    })


# ===============================
# PROFILE VIEW
# ===============================

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})


# ===============================
# EDIT PROFILE
# ===============================

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})