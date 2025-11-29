# REST Task Manager API

A modern, production-ready task management REST API built with Flask, PostgreSQL, and JWT authentication.

## Features

- **User Authentication**: Secure JWT-based authentication with access and refresh tokens
- **Task Management**: Full CRUD operations for tasks with project organization
- **Project Organization**: Group tasks under different projects
- **Status Tracking**: Track task status (pending, in_progress, completed, archived)
- **Timestamps**: Automatic created_at and updated_at tracking
- **Input Validation**: Comprehensive request validation using Marshmallow
- **Error Handling**: Consistent error responses with proper HTTP status codes
- **Database Migrations**: Alembic for database version control
- **Security**: Password hashing with bcrypt, SQL injection protection
- **API Documentation**: OpenAPI/Swagger documentation
- **Rate Limiting**: Protect endpoints from abuse
- **Logging**: Structured logging for debugging and monitoring

## Tech Stack

- **Framework**: Flask 3.0+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: Flask-JWT-Extended
- **Validation**: Marshmallow 3.0+
- **Migrations**: Alembic
- **Password Hashing**: Bcrypt
- **Environment Management**: python-dotenv

## Project Structure

```
rest-task-manager/
├── app/
│   ├── config.py                # Configuration settings
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── project.py          # Project model
│   │   └── task.py             # Task model
│   ├── schemas/
│   │   ├── user.py             # User schemas
│   │   ├── project.py          # Project schemas
│   │   └── task.py             # Task schemas
│   ├── routes/
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── projects.py         # Project endpoints
│   │   └── tasks.py            # Task endpoints
│   ├── middleware/
│   │   └── error_handlers.py  # Global error handlers
│   └── utils/
│       ├── decorators.py       # Custom decorators
│       └── helpers.py          # Helper functions
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (String, Unique, Not Null)
- `username` (String, Unique, Not Null)
- `password_hash` (String, Not Null)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Projects Table
- `id` (UUID, Primary Key)
- `name` (String, Not Null)
- `description` (Text)
- `user_id` (UUID, Foreign Key)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Tasks Table
- `id` (UUID, Primary Key)
- `title` (String, Not Null)
- `description` (Text)
- `status` (Enum: pending, in_progress, completed, archived)
- `priority` (Enum: low, medium, high)
- `due_date` (Date)
- `project_id` (UUID, Foreign Key)
- `user_id` (UUID, Foreign Key)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

### Projects
- `GET /api/projects` - List all user projects
- `POST /api/projects` - Create new project
- `GET /api/projects/:id` - Get project details
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Tasks
- `GET /api/tasks` - List all tasks (with filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/:id` - Get task details
- `PUT /api/tasks/:id` - Update task
- `PATCH /api/tasks/:id/status` - Update task status
- `DELETE /api/tasks/:id` - Delete task

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 15+
- pip and virtualenv

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd rest-task-manager
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
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Create PostgreSQL database**
```bash
psql -U postgres
CREATE DATABASE taskmanager;
CREATE USER taskmanager_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE taskmanager TO taskmanager_user;
\q
```

6. **Run database migrations**
```bash
flask db upgrade
```

7. **Run the application**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://taskmanager_user:your_password@localhost:5432/taskmanager

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Application Configuration
API_TITLE=Task Manager API
API_VERSION=1.0.0
```

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Create Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Website Redesign",
    "description": "Complete website overhaul project"
  }'
```

### Create Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Design homepage mockup",
    "description": "Create initial design concepts",
    "status": "pending",
    "priority": "high",
    "project_id": "PROJECT_UUID",
    "due_date": "2025-12-31"
  }'
```

### List Tasks with Filters
```bash
curl -X GET "http://localhost:5000/api/tasks?status=pending&priority=high&project_id=PROJECT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **CORS**: Configurable cross-origin resource sharing
- **Rate Limiting**: Prevent brute force attacks
- **Input Validation**: Marshmallow schema validation
- **Environment Variables**: Sensitive data in .env files

## Performance Considerations

- Database connection pooling
- Index optimization on frequently queried fields
- Pagination for list endpoints
- Eager loading to prevent N+1 queries
- Query result caching (optional)

## Deployment

### Using Docker
```bash
docker build -t task-manager-api .
docker run -p 5000:5000 task-manager-api
```

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub or contact the maintainers.