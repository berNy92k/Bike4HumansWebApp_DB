# 🚴 Bike Shop API

Backend for an online bike and accessories store, built with **Python and FastAPI**.  
This project was created as a practical portfolio piece to demonstrate skills in **backend development**, API design, data modeling, and modular application architecture.

The application combines:
- **REST API / backend**
- **admin panel**
- **simple Jinja-based frontend**
- **layered architecture** with clear separation of `routers`, `services`, `repositories`, `schemas`, and `models`

Admin panel:
![img.png](app/static/images/readme/admin.png)

Homepage:
![img_1.png](app/static/images/readme/homepage.png)

---

## 🛠 Technologies

- **Backend:** Python + FastAPI  
- **Database:** SQLite / relational database layer via SQLAlchemy  
- **ORM:** SQLAlchemy  
- **Testing:** pytest  
- **Server:** Uvicorn  
- **Frontend for basic UI:** Jinja templates  
- **Styling:** CSS, Bootstrap  
- **Optional:** local virtual environment for development  

---

## ✨ Highlights

- **Dedicated admin panel** for managing bikes, manufacturers, and users
- **Modular architecture** with clear separation of concerns
- **DTO-based admin workflows** with request/response schemas
- **Data validation** powered by Pydantic
- **Database migrations** handled with Alembic
- **Seeded starter data** for easier development and testing
- **Simple frontend** for presenting store content and validating functionality
- **Clean project structure** designed for easy extension

---

## 🛠 Technologies

- **Backend:** Python + FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validation / DTOs:** Pydantic
- **Testing:** pytest
- **Server:** Uvicorn
- **Frontend for basic UI:** Jinja templates
- **Styling:** CSS, Bootstrap
- **Development environment:** local virtual environment

---

## 🔑 Features

### Admin area
- Manage **bikes**, **manufacturers**, and **users**
- Full CRUD operations: **create / read / update / delete**
- Separate views, forms, and DTOs for admin workflows
- List, details, edit, and create pages for records
- Clear separation between HTTP handling and business logic

### Frontend
- Public homepage with product presentation  
- Basic layout with templates and reusable components  
- Static assets for styling and images  

### Additional Components
- Data validation with Pydantic
- Layered structure:
  - `routers` — HTTP layer
  - `services` — business logic
  - `repositories` — database access layer
  - `schemas` — input/output DTOs
  - `models` — ORM entities
- Database schema evolution through Alembic migrations
- Structure ready for additional features without mixing responsibilities

---

## 🗂 Project Structure

- `app/`
  - `main.py` — application entrypoint
  - `database/` — database connection setup
  - `models/` — ORM models for bikes, manufacturers and users
  - `repositories/` — database access layer
  - `routers/` — route definitions
    - `admin/` — admin endpoints
    - `front/` — public-facing endpoints
  - `schemas/` — Pydantic schemas
    - `admin/` — DTOs for admin operations
    - `front/` — DTOs for public views
  - `services/` — business logic
    - `admin/` — admin-related services
    - `front/` — frontend-related services
  - `templates/` — Jinja templates
    - `admin/`
    - `authentication/`
    - `front/`
  - `static/` — CSS, JS, and images
    - `css/`
    - `images/`
    - `js/`
  - `core/` — shared project utilities
- `alembic/` — database migrations
- `tests/` — automated tests
- `app.db` — local development database

---

## 🗃 Database & Migrations

The project uses **SQLite** and **Alembic** for schema migrations.  
The repository includes migrations for:
- the initial database schema
- default roles
- default users
- default manufacturers
- default bikes
- additional admin-related columns

This makes it easier to run the project locally and keep the database structure consistent.

---

## 🎯 Learning / Portfolio Goals

- Backend development with FastAPI
- REST API design
- Data modeling with SQLAlchemy
- Layered application architecture
- Separating business logic from HTTP handling
- Using Jinja templates for a simple UI
- Building a project that looks strong in a portfolio and is easy to extend

---

## 📌 Possible Next Improvements

- Expand automated tests
- Add filtering, search, and sorting
- Improve API documentation
- Enhance frontend responsiveness and UX
- Add Docker-based deployment
- Introduce a more advanced admin dashboard
