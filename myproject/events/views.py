from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count, F
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages

from .models import Event, Registration
from .forms import RegistrationForm


def event_list(request):
    """List events with filters, search, sorting, and pagination."""
    qs = Event.objects.annotate(reg_count=Count('registrations'))

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)

    status = request.GET.get('status', 'upcoming')
    now = timezone.now()
    if status == 'upcoming':
        qs = qs.filter(start_time__gte=now)
    elif status == 'past':
        qs = qs.filter(start_time__lt=now)

    cancelled = request.GET.get('cancelled')
    if cancelled == '1':
        qs = qs.filter(cancelled=True)
    elif cancelled == '0':
        qs = qs.filter(cancelled=False)

    sort = request.GET.get('sort', 'start_time')
    allowed_sorts = ['name', '-name', 'start_time', '-start_time', 'capacity', '-capacity']
    if sort not in allowed_sorts:
        sort = 'start_time'
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 8)
    page = request.GET.get('page')
    events_page = paginator.get_page(page)

    context = {
        'events': events_page,
        'q': q,
        'status': status,
        'cancelled': cancelled,
        'sort': sort,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    """Show single event details and registrations."""
    event = get_object_or_404(Event, pk=pk)
    registrations = event.registrations.all()
    form = RegistrationForm(event=event)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'registrations': registrations,
        'form': form
    })


def register_attendee(request, pk):
    """Register a user for an event."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, event=event)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.event = event
            reg.save()
            messages.success(request, "Registered successfully.")
            return redirect(reverse('events:detail', args=[event.pk]))
        else:
            registrations = event.registrations.all()
            return render(request, 'events/event_detail.html', {
                'event': event,
                'registrations': registrations,
                'form': form
            })
    return redirect(reverse('events:detail', args=[event.pk]))


def cancel_event(request, pk):
    """Toggle cancelled flag for an event."""
    event = get_object_or_404(Event, pk=pk)
    event.cancelled = not event.cancelled
    event.save()
    if event.cancelled:
        messages.info(request, "Event cancelled. New registrations are blocked.")
    else:
        messages.success(request, "Event reactivated. Registrations are open.")
    return redirect(reverse('events:detail', args=[event.pk]))


def stats_view(request):
    """Display event statistics."""
    total_events = Event.objects.count()
    total_regs = Registration.objects.count()
    upcoming = Event.objects.filter(start_time__gte=timezone.now()).count()
    cancelled = Event.objects.filter(cancelled=True).count()

    top_events = (
        Event.objects.annotate(
            reg_count=Count('registrations'),
            seats_left_calc=F('capacity') - Count('registrations')
        )
        .order_by('-reg_count')[:10]
    )

    context = {
        'total_events': total_events,
        'total_regs': total_regs,
        'upcoming': upcoming,
        'cancelled': cancelled,
        'top_events': top_events,
    }
    return render(request, 'events/stats.html', context)
