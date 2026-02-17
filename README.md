# Social Media API

A production-ready REST API for social media functionality built with FastAPI, PostgreSQL, and modern backend best practices. Features JWT authentication, vote system, comprehensive testing, and CI/CD deployment.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue.svg)](https://www.postgresql.org/)

## 🌐 Live Demo
**Disclaimer** I took down deployed api because of financial issues,I will try to deploy it with more features in future😁

**API Base URL:** [https://project1.fly.dev](https://project1.fly.dev)  
**API Documentation:** [https://project1.fly.dev/docs](https://project1.fly.dev/docs) (Interactive Swagger UI)  
**Health Check:** [https://project1.fly.dev/health](https://project1.fly.dev/health)

## 🚀 Features

- **User Authentication & Authorization**
  - JWT-based authentication with secure token generation
  - Password hashing using bcrypt
  - Protected routes with user verification

- **Post Management**
  - Create, read, update, and delete posts
  - Owner-based authorization (users can only modify their own posts)
  - Pagination and search functionality
  - Vote counting integrated with post queries

- **Voting System**
  - Upvote/downvote functionality on posts
  - Prevents duplicate votes from the same user
  - Real-time vote count aggregation

- **Security & Performance**
  - Rate limiting on critical endpoints (login, post creation, user registration)
  - CORS middleware for cross-origin requests
  - SQL injection protection via SQLAlchemy ORM
  - Comprehensive error handling

- **Database Management**
  - Alembic migrations for version control
  - PostgreSQL with proper foreign key relationships
  - SQLite support for testing environments

## 🛠️ Tech Stack

**Backend Framework:** FastAPI  
**Database:** PostgreSQL (Production), SQLite (Testing)  
**ORM:** SQLAlchemy  
**Authentication:** JWT (jose)  
**Password Hashing:** Passlib with bcrypt  
**Rate Limiting:** SlowAPI  
**Testing:** Pytest  
**Migrations:** Alembic  
**Deployment:** Docker, Fly.io  
**CI/CD:** GitHub Actions

## 📋 API Endpoints

### Authentication
- `POST /login` - User login (returns JWT token) - *Rate limited: 5/min*

### Users
- `POST /users/` - Create new user account - *Rate limited: 3/hour*
- `GET /users/{id}` - Get user by ID

### Posts
- `POST /posts/` - Create a new post (auth required) - *Rate limited: 10/min*
- `GET /posts/` - Get all posts with vote counts (supports pagination & search)
- `GET /posts/{id}` - Get specific post by ID
- `PUT /posts/{id}` - Update a post (auth required, owner only) - *Rate limited: 5/min*
- `DELETE /posts/{id}` - Delete a post (auth required, owner only)

### Votes
- `POST /vote/` - Cast or remove vote on a post (auth required) - *Rate limited: 20/min*

### Health Check
- `GET /health` - API health status

## 🔧 Installation & Setup

### Prerequisites
- Python 3.13+
- PostgreSQL
- Docker (optional)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/HarshaG2005/SOCIAL-MEDIA-API.git
cd SOCIAL-MEDIA-API
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=yourpassword
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run database migrations**
```bash
cd app
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup

```bash
docker build -t social-media-api .
docker run -p 8000:8080 social-media-api
```

## 🧪 Testing

Run the test suite:
```bash
pytest app/tests/ -v
```

Test coverage includes:
- User creation and authentication
- Post CRUD operations
- Voting functionality
- Rate limiting
- Health checks

## 📊 Database Schema

**Users Table**
- id (Primary Key)
- email (Unique)
- password (Hashed)
- created_at

**Posts Table**
- id (Primary Key)
- title
- content
- published
- created_at
- owner_id (Foreign Key → Users)

**Votes Table**
- post_id (Primary Key, Foreign Key → Posts)
- user_id (Primary Key, Foreign Key → Users)

## 🚢 Deployment

This project includes automated deployment to Fly.io via GitHub Actions.

**Deployment workflow:**
- Push to `main` branch triggers automatic deployment
- Docker image is built and deployed
- PostgreSQL database is provisioned on Fly.io

## 📝 Project Structure

```
SOCIAL-MEDIA-API/
├── app/
│   ├── routers/         # API route handlers
│   ├── tests/           # Test suite
│   ├── alembic/         # Database migrations
│   ├── main.py          # Application entry point
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── oauth2.py        # JWT authentication
│   ├── databases.py     # Database connection
│   ├── config.py        # Configuration management
│   └── utils.py         # Utility functions
├── Dockerfile
├── requirements.txt
└── fly.toml
```

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Rate limiting on sensitive endpoints
- SQL injection prevention via ORM
- Owner-based authorization for post modifications
- CORS protection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Harsha Gayantha**  
Backend Developer | FastAPI Enthusiast  
Computer Science @ University of Jaffna 🇱🇰

---

⭐ If you found this project helpful, please give it a star!
