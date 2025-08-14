from django import forms
from .models import Registration, Event

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['full_name', 'email']

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        event = self.event
        if not event:
            raise forms.ValidationError("Event not provided.")

        if event.cancelled:
            raise forms.ValidationError("This event is cancelled; registrations are closed.")

        if event.registrations_count >= event.capacity:
            raise forms.ValidationError("Event is full; no seats available.")

        if Registration.objects.filter(event=event, email__iexact=email).exists():
            raise forms.ValidationError("An attendee with this email is already registered for this event.")

        return cleaned

