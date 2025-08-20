from django.db import models

from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=0)
    cancelled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def registrations_count(self):
        return self.registrations.count()

    @property
    def seats_left(self):
        return max(self.capacity - self.registrations_count, 0)

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'email')  # ensures no duplicate email for same event
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.email})"


