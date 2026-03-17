# 🚴 Bike Shop API

Backend for an online bike and accessories store, built with **Python and FastAPI**.  
This project was created as a learning exercise, focusing on **backend development**, business logic, and REST API design. The frontend was added only to visualize functionality and test the API.

---

## 🛠 Technologies

- **Backend:** Python + FastAPI  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Migrations:** Alembic  
- **Testing:** pytest  
- **Server:** Uvicorn  
- **Dependency management:** Poetry / pipenv / requirements.txt  
- **Optional:** Docker for full-stack development  

---

## 🔑 Features

### Users
- Registration and login (JWT)  
- Roles: User/ Admin
- User profile management  

### Products
- Browse products and categories  
- Admin CRUD operations (create, update, delete)  
- Product filtering and sorting  

### Cart
- Add products to cart  
- Update quantities  
- Remove items from cart  

### Orders
- Create orders from cart  
- User order history  
- Order status: pending, paid, shipped, delivered, cancelled  
- Admin can manage all orders  

### Additional Components
- Data validation with Pydantic schemas  
- Unit and integration tests with pytest  
- Database migrations using Alembic  

---

## 🗂 Project Structure

- app/
  - main.py                  # Application entrypoint
  - core/                    # Configuration, security, custom exceptions
    - config.py
    - security.py
    - exceptions.py
  - database/                # Database configuration, sessions, migrations
    - session.py
    - base.py
    - migrations/
  - models/                  # ORM models
    - user.py
    - product.py
    - cart.py
    - order.py
  - schemas/                 # Pydantic schemas
    - user.py
    - product.py
    - cart.py
    - order.py
  - repositories/            # Database CRUD operations
    - user_repository.py
    - product_repository.py
    - cart_repository.py
    - order_repository.py
  - services/                # Business logic
    - auth_service.py
    - user_service.py
    - product_service.py
    - cart_service.py
    - order_service.py
  - routers/                 # API endpoints
    - auth_router.py
    - user_router.py
    - product_router.py
    - cart_router.py
    - order_router.py
  - dependencies/            # Dependency injection
    - auth_dependencies.py
    - database_dependencies.py

---

## 🎯 Learning Goals

- Backend development with FastAPI  
- REST API design and implementation  
- Database modeling with SQLAlchemy and PostgreSQL  
- Database migrations with Alembic  
- Writing unit and integration tests using pytest  
- Structuring a modular monolith backend for scalability  

---

## 📌 Optional Improvements

- Implement frontend with RWD (Responsive Web Design)  
- Dockerize the project for easier deployment  
- Add pagination, filtering, and search functionality  
- Integrate external services (payment, email notifications)  
- Add logging and monitoring for production readiness  
