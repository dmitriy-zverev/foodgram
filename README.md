# Foodgram - Recipe Sharing Platform

**Foodgram** is a full-stack web application that allows users to share recipes, save favorite dishes, follow other authors, and generate shopping lists based on selected recipes. The platform provides a complete recipe management system with social features.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Deployment](#deployment)

## Features

### Recipe Management
- **Create, Edit, and Delete Recipes**: Users can publish their own recipes with images, descriptions, cooking times, and ingredient lists
- **Recipe Discovery**: Browse all published recipes with pagination and filtering
- **Search & Filter**: Search recipes by name, author, tags, and ingredients
- **Recipe Details**: View complete recipe information including ingredients with amounts and cooking instructions

### User Interaction
- **User Authentication**: Secure registration and login system using email and password
- **User Profiles**: View author profiles and their published recipes
- **Follow System**: Follow favorite recipe authors to stay updated with their content
- **Favorites**: Mark recipes as favorites for quick access later

### Shopping Features
- **Shopping Cart**: Add recipes to a shopping cart
- **Shopping List Export**: Download a consolidated shopping list in CSV format with all ingredients from selected recipes
- **Ingredient Aggregation**: Automatically combines identical ingredients from multiple recipes

### Organization
- **Tags**: Categorize recipes with color-coded tags (breakfast, lunch, dinner, etc.)
- **Ingredients Database**: Comprehensive ingredient database with standardized measurement units

## Technology Stack

### Backend
- **Framework**: Django 5.2.8
- **API**: Django REST Framework 3.16.1
- **Authentication**: Djoser 2.3.3, Django REST Framework SimpleJWT 5.5.1, Token Authentication
- **Database**: PostgreSQL 14 (via psycopg2-binary)
- **Image Processing**: Pillow 12.0.0
- **Filtering**: django-filter 25.2
- **Server**: Gunicorn 23.0.0

### Frontend
- **Framework**: React (Single Page Application)
- **Build Tool**: Docker-based build process

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (reverse proxy and static file serving)
- **Database**: PostgreSQL 14

### Additional Libraries
- **API Routing**: drf-nested-routers 0.95.0
- **Social Authentication**: social-auth-app-django 5.6.0
- **Security**: cryptography 46.0.3, defusedxml 0.7.1

## Project Structure

```
foodgram/
├── backend/                      # Django backend application
│   ├── foodgram/                 # Main Django project
│   │   ├── api/                  # API routes and views
│   │   ├── core/                 # Core functionality and middleware
│   │   ├── foodgram/             # Project settings
│   │   ├── images/               # Uploaded recipe images
│   │   ├── recipes/              # Recipe models, views, serializers
│   │   └── users/                # User models and authentication
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Backend Docker configuration
│   └── manage.py                 # Django management script
├── frontend/                     # React frontend application
│   ├── src/                      # React source code
│   ├── public/                   # Static assets
│   ├── package.json              # Node dependencies
│   └── Dockerfile                # Frontend Docker configuration
├── data/                         # Initial data and fixtures
├── docs/                         # Project documentation
├── infra/                        # Infrastructure configurations
├── docker-compose.production.yml # Production Docker Compose setup
└── .env                          # Environment variables (not in repo)
```

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

For local development without Docker:
- **Python**: 3.9+
- **Node.js**: 14+
- **PostgreSQL**: 14+

## Installation & Setup

### Production Deployment with Docker

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd foodgram
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration (see [Environment Variables](#environment-variables))

3. **Build and start containers**:
   ```bash
   docker compose -f docker-compose.production.yml up -d
   ```

4. **Run migrations**:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
   ```

7. **Load initial data** (optional):
   ```bash
   docker compose -f docker-compose.production.yml exec backend python manage.py loaddata data/ingredients.json
   docker compose -f docker-compose.production.yml exec backend python manage.py loaddata data/tags.json
   ```

8. **Access the application**:
   - Frontend: http://localhost:9000
   - API: http://localhost:9000/api/
   - Admin: http://localhost:9000/admin/

### Local Development Setup

#### Backend

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**:
   - Create PostgreSQL database
   - Update database settings in `foodgram/settings.py` or use environment variables

5. **Run migrations**:
   ```bash
   cd foodgram
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial data**:
   ```bash
   python manage.py loaddata ../data/ingredients.json
   python manage.py loaddata ../data/tags.json
   ```

8. **Run development server**:
   ```bash
   python manage.py runserver
   ```

#### Frontend

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# PostgreSQL Database
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Nginx
NGINX_PORT=9000
```

**Security Notes**:
- Never commit `.env` file to version control
- Use strong, unique passwords for production
- Generate a secure SECRET_KEY for Django
- Set DEBUG=False in production

## API Documentation

### Base URL
```
http://localhost:9000/api/
```

### Authentication

The API uses Token Authentication. Include the token in the Authorization header:
```
Authorization: Token <your-token>
```

#### Obtain Token
```http
POST /api/auth/token/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Endpoints

#### Users

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/users/` | Register new user | No |
| GET | `/api/users/` | List all users | No |
| GET | `/api/users/{id}/` | Get user profile | No |
| GET | `/api/users/me/` | Get current user | Required |
| POST | `/api/users/set_password/` | Change password | Required |
| POST | `/api/users/{id}/subscribe/` | Follow user | Required |
| DELETE | `/api/users/{id}/subscribe/` | Unfollow user | Required |
| GET | `/api/users/subscriptions/` | Get followed users | Required |

#### Recipes

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/recipes/` | List recipes | No |
| POST | `/api/recipes/` | Create recipe | Required |
| GET | `/api/recipes/{id}/` | Get recipe details | No |
| PATCH | `/api/recipes/{id}/` | Update recipe | Required (author only) |
| DELETE | `/api/recipes/{id}/` | Delete recipe | Required (author only) |
| POST | `/api/recipes/{id}/favorite/` | Add to favorites | Required |
| DELETE | `/api/recipes/{id}/favorite/` | Remove from favorites | Required |
| POST | `/api/recipes/{id}/shopping_cart/` | Add to shopping cart | Required |
| DELETE | `/api/recipes/{id}/shopping_cart/` | Remove from shopping cart | Required |
| GET | `/api/recipes/download_shopping_cart/` | Download shopping list | Required |

#### Query Parameters for Recipes

- `is_favorited` (0 or 1) - Filter by favorites
- `is_in_shopping_cart` (0 or 1) - Filter by shopping cart
- `author` - Filter by author ID
- `tags` - Filter by tag slugs (can be multiple)
- `page` - Page number for pagination
- `limit` - Items per page

Example:
```
GET /api/recipes/?is_favorited=1&tags=breakfast&tags=lunch&page=1&limit=6
```

#### Tags

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/tags/` | List all tags | No |
| GET | `/api/tags/{id}/` | Get tag details | No |

#### Ingredients

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/ingredients/` | List ingredients | No |
| GET | `/api/ingredients/{id}/` | Get ingredient details | No |
| GET | `/api/ingredients/?name=onion` | Search ingredients by name | No |

### Request/Response Examples

#### Create Recipe

Request:
```http
POST /api/recipes/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
  "name": "Pasta Carbonara",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "text": "Classic Italian pasta with eggs, cheese, and pancetta",
  "cooking_time": 30,
  "tags": [1, 2],
  "ingredients": [
    {
      "id": 1,
      "amount": 400
    },
    {
      "id": 5,
      "amount": 200
    }
  ]
}
```

Response (201 Created):
```json
{
  "id": 1,
  "name": "Pasta Carbonara",
  "image": "http://localhost:9000/images/recipes/pasta.jpg",
  "text": "Classic Italian pasta with eggs, cheese, and pancetta",
  "cooking_time": 30,
  "tags": [
    {
      "id": 1,
      "name": "Lunch",
      "color": "#FF6347",
      "slug": "lunch"
    }
  ],
  "ingredients": [
    {
      "id": 1,
      "name": "Pasta",
      "measurement_unit": "g",
      "amount": 400
    }
  ],
  "author": {
    "id": 1,
    "username": "chef_mario",
    "email": "mario@example.com",
    "first_name": "Mario",
    "last_name": "Rossi"
  },
  "is_favorited": false,
  "is_in_shopping_cart": false
}
```

#### Download Shopping Cart

Request:
```http
GET /api/recipes/download_shopping_cart/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Response:
```csv
Content-Type: text/csv
Content-Disposition: attachment; filename="shopping_cart.csv"

Ingredient,Amount,Unit
Pasta,800,g
Eggs,6,pcs
Parmesan cheese,150,g
Pancetta,300,g
```

## Database Models

### User Model
- Custom user model extending AbstractUser
- Authentication using email instead of username
- Fields: username, email, first_name, last_name, password

### Recipe Model
- **Author**: ForeignKey to User
- **Name**: Recipe title (max 200 chars)
- **Image**: Recipe photo
- **Text**: Recipe description and instructions
- **Tags**: ManyToMany relationship with Tag
- **Ingredients**: ManyToMany through RecipeToIngredient
- **Cooking Time**: Positive integer (minutes)

### Tag Model
- **Name**: Tag name
- **Color**: Hex color code (#RRGGBB)
- **Slug**: URL-friendly identifier

### Ingredient Model
- **Name**: Ingredient name
- **Measurement Unit**: Unit of measurement (g, ml, pcs, etc.)

### RecipeToIngredient Model (Junction Table)
- **Recipe**: ForeignKey to Recipe
- **Ingredient**: ForeignKey to Ingredient
- **Amount**: Positive integer (quantity)

### FavoriteRecipe Model
- **User**: ForeignKey to User
- **Recipe**: ForeignKey to Recipe
- Unique together constraint on (user, recipe)

### ShoppingCart Model
- **User**: ForeignKey to User
- **Recipe**: ForeignKey to Recipe
- Unique together constraint on (user, recipe)

### Follow Model
- **Author**: User being followed
- **Follower**: User who follows
- Unique together constraint on (author, follower)

## Usage Examples

### User Registration and Authentication

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:9000/api/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "username": "johndoe",
       "first_name": "John",
       "last_name": "Doe",
       "password": "securepass123"
     }'
   ```

2. **Login to get token**:
   ```bash
   curl -X POST http://localhost:9000/api/auth/token/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "email": "john@example.com",
       "password": "securepass123"
     }'
   ```

3. **Get current user info**:
   ```bash
   curl -X GET http://localhost:9000/api/users/me/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

### Working with Recipes

1. **Browse recipes**:
   ```bash
   curl -X GET "http://localhost:9000/api/recipes/?page=1&limit=6"
   ```

2. **Filter recipes by tags**:
   ```bash
   curl -X GET "http://localhost:9000/api/recipes/?tags=breakfast&tags=quick"
   ```

3. **Search ingredients**:
   ```bash
   curl -X GET "http://localhost:9000/api/ingredients/?name=tomato"
   ```

4. **Add recipe to favorites**:
   ```bash
   curl -X POST http://localhost:9000/api/recipes/1/favorite/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

5. **Add recipe to shopping cart**:
   ```bash
   curl -X POST http://localhost:9000/api/recipes/1/shopping_cart/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

6. **Download shopping list**:
   ```bash
   curl -X GET http://localhost:9000/api/recipes/download_shopping_cart/ \
     -H "Authorization: Token YOUR_TOKEN" \
     -o shopping_list.csv
   ```

### Social Features

1. **Follow a user**:
   ```bash
   curl -X POST http://localhost:9000/api/users/2/subscribe/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

2. **Get list of followed users**:
   ```bash
   curl -X GET http://localhost:9000/api/users/subscriptions/ \
     -H "Authorization: Token YOUR_TOKEN"
   ```

3. **View user's recipes**:
   ```bash
   curl -X GET "http://localhost:9000/api/recipes/?author=2"
   ```

## Development

### Running Tests

Backend tests:
```bash
cd backend/foodgram
python manage.py test
```

### Code Quality

The project follows PEP 8 style guidelines for Python code. Check code quality:
```bash
flake8 backend/
```

### Database Migrations

Create new migrations after model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel

Access Django admin panel at http://localhost:9000/admin/ to:
- Manage users
- Create/edit tags and ingredients
- Moderate recipes
- View all database models

### Useful Django Commands

```bash
# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Check project for issues
python manage.py check

# Generate fixtures
python manage.py dumpdata recipes.Tag --indent 2 > tags.json
python manage.py dumpdata recipes.Ingredient --indent 2 > ingredients.json
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Configure proper `SECRET_KEY`
- [ ] Set up secure `ALLOWED_HOSTS`
- [ ] Use strong database credentials
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper CORS settings
- [ ] Configure media and static file serving
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Review security middleware settings

### Docker Compose Services

#### db (PostgreSQL)
- Image: postgres:14
- Persistent volume for data storage
- Environment configuration via .env

#### backend (Django)
- Custom image: dmitriyvzverev/foodgram_backend
- Serves REST API
- Connected to PostgreSQL
- Volumes: static files, media files

#### frontend (React)
- Custom image: dmitriyvzverev/foodgram_frontend
- Serves Single Page Application
- Static files volume

#### nginx
- Custom image: dmitriyvzverev/foodgram_nginx
- Reverse proxy
- Serves static and media files
- Port mapping: 9000:80

### Scaling Considerations

- Use Redis for caching frequently accessed data
- Implement Celery for asynchronous tasks (email notifications, report generation)
- Set up CDN for static and media files
- Configure database connection pooling
- Use gunicorn with multiple workers
- Implement rate limiting for API endpoints

### Monitoring

Consider implementing:
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Log aggregation (ELK stack)
- Uptime monitoring
- Database query optimization

## Contributing

Contributions are welcome! Please ensure:
- Code follows project style guidelines
- All tests pass
- New features include tests
- Documentation is updated
- Commit messages are clear and descriptive

---

**Project Status**: Active Development

**Last Updated**: November 2025

For questions or issues, please open an issue in the repository.
