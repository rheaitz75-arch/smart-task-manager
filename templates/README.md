# Smart Task Management System

## Overview
The Smart Task Management System is a Python Flask-based web application that helps users manage their daily tasks efficiently.

The application includes:
- User Authentication
- Task Management
- REST APIs
- PostgreSQL Database Integration
- Analytics Dashboard
- WebSocket Notifications
- Responsive UI

---

## Features

### Authentication
- User Registration
- User Login
- Logout Functionality

### Task Management
- Add Task
- Update Task
- Delete Task
- View All Tasks

### Analytics
Using Pandas and NumPy:
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage

### WebSocket Feature
- Real-time notification when a new task is added

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- PostgreSQL
- Pandas
- NumPy
- HTML
- CSS
- Bootstrap 5

---

## Project Structure

smart-task-manager/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ └── update_task.html
│
└── static/
└── style.css

---

## Installation Steps

### Clone Repository

```bash
git clone <repository-link>