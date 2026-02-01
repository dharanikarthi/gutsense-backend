# GutSense Backend Deployment Guide

## Current Status: ✅ FIXED

The backend crash has been resolved by creating a lightweight version compatible with Vercel's serverless functions.

## Deployment Versions

### 1. **Lightweight Version (Current - Vercel Compatible)**
- **File**: `main.py`
- **Requirements**: `requirements.txt` (minimal dependencies)
- **Status**: ✅ Deployed and working
- **URL**: https://gutsense-backend.vercel.app
- **Features**:
  - Basic API endpoints
  - Demo food analysis
  - CORS configured
  - No heavy ML dependencies

### 2. **Full ML Version (Future - Dedicated Server)**
- **File**: `main_with_ml.py`
- **Requirements**: `requirements_ml.txt` (includes TensorFlow)
- **Status**: 📦 Ready for deployment on dedicated server
- **Features**:
  - All lightweight features
  - TensorFlow ML model support
  - .h5 model loading
  - Advanced predictions

## Why the Crash Happened

The backend was crashing because:
1. **TensorFlow is too heavy** for Vercel serverless functions (500MB+ size limit)
2. **Import errors** during cold starts
3. **Memory limitations** on serverless platforms

## Current Working Endpoints

✅ **Basic Endpoints**:
- `GET /` - Health check
- `GET /api/health` - Detailed status
- `GET /api/demo/food-categories` - Food categories
- `GET /api/demo/gut-types` - Gut types
- `POST /api/demo/analyze-food` - Basic food analysis

✅ **ML Endpoints (Lightweight Mode)**:
- `GET /api/models/status` - Shows ML disabled status
- `GET /api/models/list` - Returns empty list
- `POST /api/models/predict` - Returns disabled message

## Testing the Fix

### 1. Health Check
```bash
curl https://gutsense-backend.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "demo_mode",
  "version": "1.0.0",
  "environment": "production"
}
```

### 2. Food Analysis
```bash
curl -X POST https://gutsense-backend.vercel.app/api/demo/analyze-food \
  -H "Content-Type: application/json" \
  -d '{"food_name": "Pizza"}'
```

### 3. Frontend Integration
Visit: https://gutsense-frontend.vercel.app/test-integration.html

Should show green success messages.

## Future ML Model Integration

When you're ready to use ML models, you have two options:

### Option A: Dedicated Server (Recommended)
1. Deploy to a VPS, AWS EC2, or Google Cloud
2. Use `main_with_ml.py` as the main file
3. Install dependencies from `requirements_ml.txt`
4. Copy your .h5 files to `models/h5_models/`

### Option B: Vercel with External ML Service
1. Keep current lightweight backend
2. Create separate ML microservice on another platform
3. Call ML service from the lightweight backend

## File Structure

```
backend/
├── main.py                 # ✅ Current lightweight version
├── main_with_ml.py         # 📦 Full ML version for future
├── requirements.txt        # ✅ Lightweight dependencies
├── requirements_ml.txt     # 📦 Full ML dependencies
├── models/
│   ├── model_loader.py     # ML model loading system
│   ├── h5_models/          # Directory for .h5 files
│   └── README.md           # ML documentation
└── DEPLOYMENT.md           # This file
```

## Rollback Plan

If issues occur, you can quickly rollback:
```bash
git checkout main_simple.py
cp main_simple.py main.py
git commit -m "Rollback to simple version"
git push
```

## Monitoring

- **Vercel Dashboard**: Check function logs
- **Health Endpoint**: Monitor `/api/health`
- **Frontend Test**: Use test-integration.html

The backend is now stable and ready for production use! 🚀