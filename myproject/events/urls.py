from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='list'),
    path('event/<int:pk>/', views.event_detail, name='detail'),
    path('event/<int:pk>/register/', views.register_attendee, name='register'),
    path('event/<int:pk>/cancel/', views.cancel_event, name='cancel'),
    path('stats/', views.stats_view, name='stats'),
]
