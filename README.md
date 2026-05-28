# HouseTasks

A Django web app for shared households to organize and track cleaning tasks. Users create or join a "House", invite/approve members, and assign weekly cleaning tasks to specific members.

## Features

- User registration, login, and logout
- Create a House or request to join an existing one
- House owners/members can approve or reject join requests
- Add, edit, delete cleaning tasks
- Assign tasks to one or more household members
- Mark tasks as done / unmark done
- Tracks the ISO week the task was started

## Tech Stack

- Python / Django 6.0
- SQLite (default, `db.sqlite3`)
- HTML templates + static assets

## Project Structure

```
HouseTasks/
├── HouseTasks/          # Django project settings (settings.py, urls.py, wsgi.py)
├── tasks/               # Main app: models, views, urls
│   ├── models.py        # House, Cleaning_Task
│   ├── views.py         # Auth + house/task CRUD
│   └── urls.py
├── templates/           # homepage/, house/, tasks/
├── static/              # CSS / JS / images
├── db.sqlite3
└── manage.py
```

## Models

- **House** — `housename`, `members` (M2M User), `request` (M2M User pending join requests)
- **Cleaning_Task** — `name`, `description`, `user_added`, `date`, `start_week`, `assigned_members` (M2M User), `done`, `House` (id)

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Setup

```powershell
# from the repo root
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django

cd HouseTasks
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

## Main Routes

| Path | Purpose |
|------|---------|
| `/` | Homepage |
| `/register`, `/login`, `/logout` | Auth |
| `/buildhouse/` | Create a new house |
| `/enterhouse` | Enter a house you belong to |
| `/request_join` | Request to join a house |
| `/house/<id>` | House dashboard |
| `/members/<id>` | Manage members and join requests |
| `/cleaning/<id>` | List / add cleaning tasks |
| `/task_action/<id>` | Mark done / unmark / delete / edit selected tasks |
| `/edit_task/<id>` | Save edits to selected tasks |

## Notes

- `ALLOWED_HOSTS` is empty; set it for any non-local host.
