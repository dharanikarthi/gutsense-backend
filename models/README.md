# GutSense ML Models

This directory contains machine learning models for the GutSense application.

## Directory Structure

```
models/
├── __init__.py
├── model_loader.py          # Model loading and prediction utilities
├── h5_models/              # Directory for .h5 model files
│   ├── .gitkeep
│   └── [your-model].h5     # Place your .h5 files here
└── README.md               # This file
```

## How to Add Your .h5 Models

### Step 1: Copy Your .h5 Files
1. Locate your `.h5` folder on the desktop
2. Copy all `.h5` files from that folder
3. Paste them into the `backend/models/h5_models/` directory

### Step 2: Manual Copy Instructions
Since the terminal is having issues, please manually:

1. **Open File Explorer**
2. **Navigate to**: `C:\Users\kmage\OneDrive\Desktop\GutSense\backend\models\h5_models\`
3. **Find your .h5 folder** on the desktop
4. **Copy all .h5 files** from your desktop folder
5. **Paste them** into the `h5_models` directory

### Step 3: Verify Installation
After copying the files, you can test the models using these API endpoints:

- `GET /api/models/list` - List all available models
- `GET /api/models/status` - Check ML system status
- `POST /api/models/predict` - Make predictions with a model

## API Endpoints

### List Available Models
```bash
GET /api/models/list
```
Response:
```json
{
  "models": ["model1", "model2"],
  "count": 2,
  "status": "success"
}
```

### Check Model Status
```bash
GET /api/models/status
```
Response:
```json
{
  "tensorflow_available": true,
  "tensorflow_version": "2.15.0",
  "model_loader_available": true,
  "available_models": ["model1", "model2"],
  "model_count": 2
}
```

### Make Prediction
```bash
POST /api/models/predict
Content-Type: application/json

{
  "model_name": "your_model_name",
  "input_data": [[1, 2, 3, 4, 5]]
}
```

Response:
```json
{
  "prediction": [[0.8, 0.2]],
  "model_used": "your_model_name",
  "status": "success"
}
```

## Model Naming Convention

- Model files should be named descriptively (e.g., `food_classifier.h5`, `gut_health_predictor.h5`)
- The API will use the filename (without .h5 extension) as the model name
- Example: `food_classifier.h5` → model name: `food_classifier`

## Dependencies

The following packages are required for ML model support:
- `tensorflow==2.15.0`
- `numpy==1.24.3`
- `pandas==2.0.3`

These are already included in `requirements.txt`.

## Troubleshooting

### Model Not Loading
1. Check that the .h5 file is in the correct directory
2. Verify the file is not corrupted
3. Check the API logs for specific error messages

### TensorFlow Issues
1. Ensure TensorFlow is installed: `pip install tensorflow==2.15.0`
2. Check compatibility with your system
3. For Vercel deployment, TensorFlow should install automatically

### File Path Issues
- Use forward slashes in paths: `models/h5_models/model.h5`
- Ensure no spaces in filenames
- Use lowercase names when possible

## Example Usage

```python
# In your application code
from models.model_loader import model_loader

# Load and use a model
result = model_loader.predict("food_classifier", input_data)
print(result)
```