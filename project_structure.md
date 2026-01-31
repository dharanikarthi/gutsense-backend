# GutSense Backend Project Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database connection and session
│   ├── models.py                # SQLAlchemy database models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── auth.py                  # Authentication utilities
│   ├── food_engine.py           # Rule-based food analysis engine
│   └── routers/                 # API route handlers
│       ├── __init__.py
│       ├── auth.py              # Authentication endpoints
│       ├── gut_profile.py       # Gut profile management
│       └── food_analysis.py     # Food analysis endpoints
│
├── scripts/                     # Utility scripts
│   ├── start_dev.py            # Development server starter
│   └── test_api.py             # API testing script
│
├── alembic/                     # Database migrations (auto-generated)
│   └── versions/
│
├── main.py                      # FastAPI application entry point
├── setup_db.py                  # Database setup script
├── quick_start.py               # One-command setup script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── Dockerfile                   # Docker container configuration
├── docker-compose.yml           # Docker Compose setup
├── alembic.ini                  # Database migration configuration
├── README.md                    # Project documentation
└── project_structure.md         # This file
```

## Key Components

### 🔧 Core Application (`app/`)
- **config.py**: Environment variables and settings management
- **database.py**: SQLAlchemy database connection and session handling
- **models.py**: Database table definitions (User, GutProfile, FoodAnalysis)
- **schemas.py**: Pydantic models for API request/response validation
- **auth.py**: JWT authentication, password hashing, user verification
- **food_engine.py**: Rule-based food analysis logic

### 🛣️ API Routes (`app/routers/`)
- **auth.py**: User registration, login, token management
- **gut_profile.py**: Gut profile CRUD operations
- **food_analysis.py**: Food analysis, history, statistics

### 🚀 Entry Points
- **main.py**: FastAPI app initialization and configuration
- **setup_db.py**: Database and table creation
- **quick_start.py**: Automated setup for development

### 🧪 Development Tools (`scripts/`)
- **start_dev.py**: Development server with auto-reload
- **test_api.py**: Automated API endpoint testing

### 🐳 Deployment
- **Dockerfile**: Container image definition
- **docker-compose.yml**: Multi-service deployment (API + PostgreSQL)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Gut Profiles Table
```sql
CREATE TABLE gut_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    gut_type VARCHAR NOT NULL,  -- balanced, high_inflammation, low_diversity
    sensitivities TEXT,         -- comma-separated: acidity,ibs,lactose
    spice_tolerance INTEGER DEFAULT 2,  -- 1=low, 2=medium, 3=high
    additional_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### Food Analyses Table
```sql
CREATE TABLE food_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    food_name VARCHAR NOT NULL,
    food_category VARCHAR,
    reaction VARCHAR NOT NULL,  -- suitable, caution, avoid
    explanation TEXT NOT NULL,
    alternatives TEXT,          -- JSON array
    confidence_score INTEGER DEFAULT 85,
    reported_symptoms TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints Overview

### Authentication (`/api/auth/`)
- `POST /signup` - Register new user
- `POST /login` - User authentication
- `GET /me` - Get current user info
- `POST /logout` - User logout
- `POST /refresh` - Refresh JWT token

### Gut Profile (`/api/gut-profile/`)
- `POST /` - Create/update gut profile
- `GET /` - Get user's gut profile
- `PUT /` - Update gut profile
- `DELETE /` - Delete gut profile
- `GET /gut-types` - Available gut types
- `GET /sensitivities` - Available sensitivities

### Food Analysis (`/api/food/`)
- `POST /analyze` - Analyze food compatibility
- `GET /history` - Get analysis history
- `GET /history/{id}` - Get specific analysis
- `DELETE /history/{id}` - Delete analysis
- `DELETE /history` - Clear all history
- `GET /stats` - User statistics
- `GET /search` - Search foods

## Rule-Based Analysis Logic

The food analysis engine uses simple IF-ELSE rules:

```python
# Sensitivity-based rules
IF "lactose" in sensitivities AND "dairy" in food_categories:
    RETURN "avoid"

# Gut type rules
IF gut_type == "high_inflammation" AND "fried" in food_categories:
    RETURN "avoid"

# Spice tolerance rules
IF spice_tolerance == 1 AND "spicy" in food_categories:
    RETURN "avoid"
```

## Development Workflow

1. **Setup**: Run `python quick_start.py`
2. **Development**: Use `python scripts/start_dev.py`
3. **Testing**: Run `python scripts/test_api.py`
4. **Documentation**: Visit `http://localhost:8000/docs`

## Deployment Options

1. **Local Development**: `python main.py`
2. **Docker**: `docker-compose up`
3. **Production**: Deploy to cloud with environment variables

This structure provides a clean, modular, and scalable foundation for the GutSense backend API.