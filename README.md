# 🗓️ Django Event Registration System

A simple Django web application for managing events, attendee registrations, and event statistics.  
Includes features for event listing, filtering, sorting, pagination, registration management, cancellation, and admin event creation.

---

## Features
- Create, update, and delete events (via Django Admin)
- List events with:
  - Search
  - Status filter (upcoming, past)
  - Cancelled filter
  - Sorting by name, date, or capacity
  - Pagination
- View event details & registrations
- Register attendees with:
  - Duplicate email prevention
  - Event capacity limit
  - Block registration if cancelled
- Cancel/reactivate events
- Statistics dashboard with:
  - Total events
  - Total registrations
  - Upcoming events
  - Cancelled events
  - Top events by registrations

---

Tech Stack
- **Backend:** Django 5+ (Python 3.10+)
- **Database:** SQLite (default) — can be changed to PostgreSQL/MySQL
- **Frontend:** HTML, Bootstrap 5, Django Templates

---
