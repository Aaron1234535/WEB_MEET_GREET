from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # Profile
    path('profile/', views.profile_view, name='profile'),   # 👈 ADD THIS
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),

    # Event Detail
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    # RSVP
    path('events/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),

    # Event Photos
   path(
    'events/<int:event_id>/photos/add/',
    views.upload_event_photo,
    name='upload_event_photo'
),

    # My Events
    path('my-events/', views.my_events, name='my_events'),
    
    path('events/<int:event_id>/like/', views.like_event, name='like_event'),
]