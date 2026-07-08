# 💰 Personal Finance Tracker

A Flask-based Personal Finance Tracker developed as part of my internship project.

---

## ✨ Features

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

## 🛠 Tech Stack

- Python 3.12
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

## 📂 Project Structure

```text
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

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/sharweshvar333/Personal-Finance-Tracker.git
cd Personal-Finance-Tracker
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python run.py
```

---

## 🐳 Running with Docker

### Build the Docker image

```bash
docker build -t finance-tracker .
```

### Run the container

```bash
docker run -p 5000:5000 finance-tracker
```

### Open the application

```
http://localhost:5000
```

---

## ✅ Testing

Run all tests

```bash
pytest
```

---

## 👨‍💻 Author

**Sharweshvar P**

Internship Project – Personal Finance Tracker
