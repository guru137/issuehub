# 🚀 IssueHub – Lightweight Bug Tracker

## 📌 Overview

IssueHub is a full-stack bug tracking system where users can create projects, manage issues, assign tasks, track status, and collaborate via comments.

---

## 🛠 Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* SQLite (can switch to PostgreSQL)
* Alembic (migrations)
* JWT Authentication

### Frontend

* React (Vite)
* Axios
* React Router

---

## 🔐 Features

### Authentication

* User signup & login
* JWT-based authentication
* Protected routes

---

### Projects

* Create project
* View projects

---

### Issues

* Create issue
* Update issue
* Delete issue
* Assign user
* Change status (open, in_progress, closed)
* Set priority (low, medium, high, critical)

---

### Comments

* Add comments on issues
* View comment threads

---

### Advanced Features

* Search issues by title
* Filter by status & assignee
* Sort issues (created_at, priority, status)

---

## 📂 Project Structure

### Backend

```
app/
  main.py
  models/
  schemas/
  routes/
  core/
  db/
```

### Frontend

```
issuehub-frontend/
  src/
    pages/
    components/
    services/
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-link>
cd issuehub
```

---

### 2. Backend Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run server:

```
uvicorn app.main:app --reload
```

---

### 3. Frontend Setup

```
cd issuehub-frontend
npm install
npm run dev
```

Open:

```
http://localhost:5173
```

---

## 🔑 Environment Variables

Create `.env` file:

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./test.db
```

---

## 📡 API Overview

* POST /signup
* POST /login
* GET /projects
* POST /projects
* GET /issues/{project_id}
* POST /issues
* PATCH /issues/{id}
* DELETE /issues/{id}
* GET /comments/{issue_id}
* POST /comments/{issue_id}

---

## 🧪 Testing

Basic API testing done using Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🚧 Known Limitations

* No project member roles (maintainer/user)
* UI is basic (not styled professionally)
* No automated tests implemented

---

## 🚀 Future Improvements

* Add project members & roles
* Improve UI/UX
* Add pagination
* Add notifications
* Add automated testing

---

## 👨‍💻 Author

Developed by Gogula Naga Guravaiah

---
