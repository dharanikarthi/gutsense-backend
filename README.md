# GutSense Backend API

A FastAPI-based backend for an AI-powered gut health food advisor using rule-based logic.

## 🚀 Features

- **User Authentication**: JWT-based signup/login system
- **Gut Profile Management**: Store and manage user gut health profiles
- **Food Analysis**: Rule-based food compatibility analysis
- **Food History**: Track and analyze food consumption patterns
- **RESTful API**: Clean, documented API endpoints

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Secure authentication tokens
- **Uvicorn**: ASGI server for production

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gutsense-backend
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
   # Edit .env with your database credentials
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Create database user and database
   sudo -u postgres psql
   CREATE USER gutsense_user WITH PASSWORD 'your_password';
   CREATE DATABASE gutsense_db OWNER gutsense_user;
   GRANT ALL PRIVILEGES ON DATABASE gutsense_db TO gutsense_user;
   \q
   ```

6. **Initialize database**
   ```bash
   python setup_db.py
   ```

7. **Start the server**
   ```bash
   python main.py
   ```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh JWT token

### Gut Profile
- `POST /api/gut-profile/` - Create/update gut profile
- `GET /api/gut-profile/` - Get user's gut profile
- `PUT /api/gut-profile/` - Update gut profile
- `DELETE /api/gut-profile/` - Delete gut profile
- `GET /api/gut-profile/gut-types` - Get available gut types
- `GET /api/gut-profile/sensitivities` - Get available sensitivities

### Food Analysis
- `POST /api/food/analyze` - Analyze food compatibility
- `GET /api/food/history` - Get food analysis history
- `GET /api/food/history/{id}` - Get specific analysis
- `DELETE /api/food/history/{id}` - Delete analysis
- `DELETE /api/food/history` - Clear all history
- `GET /api/food/stats` - Get user food statistics
- `GET /api/food/search` - Search foods

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique user email
- `name`: User's full name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Gut Profiles Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `gut_type`: balanced, high_inflammation, low_diversity
- `sensitivities`: Comma-separated sensitivity list
- `spice_tolerance`: 1 (low), 2 (medium), 3 (high)
- `additional_notes`: User notes
- `created_at`, `updated_at`: Timestamps

### Food Analyses Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `food_name`: Name of analyzed food
- `food_category`: Food category
- `reaction`: suitable, caution, avoid
- `explanation`: Analysis explanation
- `alternatives`: JSON array of alternatives
- `confidence_score`: Analysis confidence (0-100)
- `reported_symptoms`: User-reported symptoms
- `created_at`: Timestamp

## 🧠 Rule-Based Analysis Engine

The food analysis uses simple IF-ELSE logic:

```python
# Example rules
IF gut_type == "high_inflammation" AND food_category == "fried":
    RETURN "avoid"

IF "lactose" in sensitivities AND "dairy" in food_categories:
    RETURN "avoid"

IF spice_tolerance == 1 AND "spicy" in food_categories:
    RETURN "avoid"
```

### Food Categories
- **High Inflammation**: Fried foods, processed meats
- **Spicy**: Curry, chili, hot sauce
- **Dairy**: Milk, cheese, yogurt
- **Acidic**: Tomatoes, citrus, coffee
- **High Fiber**: Beans, whole grains
- **Gentle**: Rice, banana, chicken breast

## 🔒 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with expiration
- **CORS Protection**: Configurable cross-origin requests
- **Input Validation**: Pydantic schemas for data validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Test API endpoints
curl -X POST "http://localhost:8000/api/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com", "password": "testpass123"}'
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚀 Deployment

### Vercel Deployment (Recommended)

This backend is configured for easy deployment on Vercel:

1. **Push to GitHub** (already done)
   ```bash
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository: `dharanikarthi/gutsense-backend`
   - Vercel will automatically detect the Python project
   - Set environment variables in Vercel dashboard:
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `SECRET_KEY`: Your JWT secret key
     - `DEBUG`: `False`

3. **Environment Variables for Vercel**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:5432/db
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   HOST=0.0.0.0
   PORT=8000
   ```

### Using Docker (Optional)
```bash
# Build image
docker build -t gutsense-api .

# Run container
docker run -p 8000:8000 gutsense-api
```

### Database for Production
For production deployment, consider using:
- **Vercel Postgres**: Integrated PostgreSQL database
- **Supabase**: Free PostgreSQL with additional features
- **Railway**: Simple PostgreSQL hosting
- **Neon**: Serverless PostgreSQL

## 🔄 Future Enhancements

1. **Machine Learning Integration**: Replace rule-based engine with ML models
2. **Image Analysis**: Add food image recognition
3. **Nutritional Data**: Integrate with nutrition APIs
4. **Caching**: Add Redis for performance
5. **Rate Limiting**: Implement API rate limiting
6. **Logging**: Add comprehensive logging
7. **Testing**: Add unit and integration tests

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify credentials in `.env`
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in `.env`: `PORT=8001`
   - Or kill process: `lsof -ti:8000 | xargs kill -9`

### Getting Help

- Check the API documentation at `/docs`
- Review error logs in the console
- Ensure all environment variables are set correctly

## 📞 Contact

For questions or support, please open an issue in the repository.