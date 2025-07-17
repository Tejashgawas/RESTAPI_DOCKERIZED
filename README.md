# 📚 Flask REST API – Book Management System

A production-ready RESTful API built with Flask for managing books, including features like JWT authentication, pagination, sorting, search, and Docker support. The API is organized using Blueprints, follows best practices, and is fully containerized.

---

## 🚀 Features

- 🔐 JWT Authentication with Refresh Tokens
- 🧠 Role-based Access (Admin/User)
- 📚 Book CRUD operations
- 🔍 Advanced filtering:
  - Pagination (`?page=1&per_page=5`)
  - Sorting (`?sort=asc` or `desc`)
  - Search (`?search=python`)
- 🧪 Pytest-based Unit Testing
- 📦 Docker + Docker Compose support
- ⚙️ Environment Variables via `.env`
- 🗃️ Alembic Migrations (SQLite)
- ✅ Swagger UI with `flasgger`

---

## 📁 Project Structure

```
RESTAPI/
│
├── app/
│ ├── models/ # SQLAlchemy models
│ ├── routes/ # Blueprints (auth, book)
│ ├── schemas/ # Marshmallow schemas
│ ├── utils/ # Helper functions (auth, Redis)
│ ├── tests/ # Pytest-based tests
│ ├── config.py # Configuration loader
│ └── init.py # App factory
│
├── instance/
│ └── books.db # SQLite database
│
├── migrations/ # Alembic migrations
├── .env # Environment variables (excluded from git)
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py # Entry point
└── seed.py # Seed script for DB
```

---

## 🐳 Docker Setup

### 1. ✅ Build and Start Container

```
docker-compose up --build
```
## 📬 Access the API
```
Visit: http://localhost:5000
Swagger UI: http://localhost:5000/apidocs\
```

Make sure .env file exists before building (but don't push it to GitHub).

## 🔐 Authentication (JWT)
```
- Login: /auth/login
- OAUTH login : /auth/google-login

- Register: /auth/register

- Access Protected Route:/auth/profile
(for postman needed token  in header)

- Refresh Token: /auth/refresh
- logout : /auth/logout
```

📘 Book API (with enhancements)
Method	Endpoint	Description
```
GET	/books	List books (with pagination, sort, search)
POST	/books	Create a book (Admin only)
GET	/books/<id>	Get single book
PUT	/books/<id>	Update book (Admin only)
DELETE	/books/<id>	Delete book (Admin only)
```

Query Examples
```
GET /books?search=python&sort=asc&page=1&per_page=3
```
🧪 Run Tests
```
pytest
```
⚙️ Environment Variables (.env)
```
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///instance/books.db
GOOGLE_CLIENT_ID =your_client_id
GOOGLE_CLIENT_SECRET_KEY = yous_google_secret_key
REDIS_URL=redis://localhost:6379/0
Do NOT push .env to GitHub.
```
🐙 Deployment Notes
- Use Docker for production deployment.
- Add reverse proxy (e.g. Nginx) + SSL in production.

Replace SQLite with PostgreSQL for scalability.
- 🧠 Future Enhancements
- 📦 PostgreSQL integration
- 📈 Admin Dashboard
- 📬 Email verification, password reset

👨‍💻 Author
- Tejash Gawas
- 📍 Vasco, Goa
- 📬 @tejlogs

🛡️ License
MIT – Use freely, credit appreciated.
---

Let me know if you want a GitHub Actions workflow, contribution guide, or OpenAPI.json export for this too.








