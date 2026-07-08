# 💰 Personal Finance Tracker

A Flask-based Personal Finance Tracker developed as part of my internship project.

---

## Features

- User Registration & Login
- Income & Expense Tracking
- Budget Management
- Dashboard with Charts
- Monthly Summary
- CSV Import & Export
- PDF Report Generation
- REST API
- Exchange Rate Integration
- Rate Limiting
- Docker Support
- Gunicorn Deployment

---

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- Flask-Login
- Flask-WTF
- Bootstrap
- Docker
- Gunicorn
- Git & GitHub

---

## Project Structure

```
app/
│
├── blueprints/
├── services/
├── templates/
├── static/
├── extensions.py
└── __init__.py

tests/
docs/
run.py
config.py
requirements.txt
Dockerfile
docker-compose.yml
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/sharweshvar333/Personal-Finance-Tracker.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python run.py
```

---

## Docker

Build and start

```bash
docker compose up --build
```

---

## Testing

Run tests

```bash
pytest
```

---

## Author

Sharweshvar P

Internship Project – Personal Finance Tracker

## Running with Docker

Build

docker build -t finance-tracker .

Run

docker run -p 5000:5000 finance-tracker

Open

http://localhost:5000