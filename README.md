# BE-BookMyShow-OmJindal

## BookYourShow (Backend)

A modern, Django backend for **BookMyShow**, built with Django REST Framework, PostgreSQL, JWT authentication.

---

## 🛠️ Tech Stack

- **Python** – Backend language
- **Django** – Core backend framework
- **Django REST Framework** – API layer
- **PostgreSQL** – Database
- **JWT (SimpleJWT)** – Authentication
- **uv** – Dependency & virtual environment manager

---

## 🚀 Apps

- **Base** – Shared utilities and base models
- **User** – Authentication and user management
- **Cinema** – Cinema and Seats
- **Movie** – Movie to be screened
- **Slot** – Show timings and seat availability
- **Booking** – Seat booking and history

---

## 📁 Folder Structure

```
project-root/
│
├── main.py
├── manage.py
├── pyproject.toml
├── uv.lock
├── .env-template
├── .gitignore
├── .python-version
│
├── bookmyshow
│ ├── settings.py
│ └── urls.py
| └── asgi.py
| └── wsgi.py
│
├── apps
│ ├── base
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      ├── utils.py
│ |      └── views.py
│ ├── user
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      ├── utils.py
│ |      └── views.py
│ ├── cinema
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      ├── utils.py
│ |      └── views.py
│ ├── movie
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      ├── utils.py
│ |      └── views.py
│ ├── slot
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      ├── utils.py
│ |      └── views.py
│ └── booking
│ |      ├── migrations
│ |      ├── admin.py
│ |      ├── apps.py
│ |      ├── constants.py
│ |      ├── models.py
│ |      ├── serializers.py
│ |      ├── tests.py
│ |      ├── urls.py
│ |      └── views.py
│
└── README.md
```

---

## 🧩 Getting Started

### Prerequisites

- **Python**: Version **3.10**  
  Download from [https://www.python.org](https://www.python.org)

- **uv**: Python package manager & virtual environment tool

  ```bash
  pip install uv
  ```

### Installation

Follow these steps to set up the backend locally.

1.  **Clone the Repository**

    ```
    git clone <repository-url>
    cd <project-folder>
    ```

2.  **Create Virtual Environment & Install Dependencies**

    ```bash
    uv sync --all-groups
    ```

3.  **Setup Environment Variables**

    Create a `.env` file at the root level using `.env-template` as reference.

4.  **Run Database Migrations**

    ```bash
    uv run python manage.py migrate
    ```

5.  **Start the Development Server**

    ```bash
    uv run python manage.py runserver
    ```

    The backend will be available at:

    ```
    http://localhost:8000
    ```

## 🧹 Code Quality

- **Ruff** is used for linting, formatting, and import sorting
- Configured via `pyproject.toml`
- Runs in development only

### Common Commands

```bash
# Lint code
uv run ruff check .

# Auto-fix lint issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```
