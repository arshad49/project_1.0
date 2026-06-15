"""
FastAPI Application for Crop Disease Detection System
Provides REST API endpoints for disease prediction
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from pathlib import Path

from prediction_service import get_prediction_service
from config import API_HOST, API_PORT


# Initialize FastAPI app
app = FastAPI(
    title="Crop Disease Detection System",
    description="AI-powered crop disease detection using deep learning",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global prediction service
prediction_service = None


class PredictionResponse(BaseModel):
    """Response model for prediction"""
    success: bool
    predicted_class: Optional[str] = None
    crop_type: Optional[str] = None
    disease_status: Optional[str] = None
    confidence: Optional[float] = None
    is_healthy: Optional[bool] = None
    top_3_predictions: Optional[List[dict]] = None
    recommendation: Optional[str] = None
    urgency: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    loaded: bool


@app.on_event("startup")
async def startup_event():
    """Initialize prediction service on startup"""
    global prediction_service
    prediction_service = get_prediction_service()
    
    # Try to load the model
    loaded = prediction_service.load()
    
    if loaded:
        print(f"✓ Prediction service loaded successfully")
    else:
        print("⚠ Warning: Model not loaded. Please train the model first.")


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy" if prediction_service and prediction_service.is_loaded else "degraded",
        message="Crop Disease Detection System API",
        loaded=prediction_service.is_loaded if prediction_service else False
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    return HealthResponse(
        status="ok" if prediction_service and prediction_service.is_loaded else "error",
        message="System operational" if prediction_service and prediction_service.is_loaded else "Model not loaded",
        loaded=prediction_service.is_loaded if prediction_service else False
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)):
    """
    Predict crop disease from uploaded image
    
    - **file**: Image file (jpg, jpeg, png)
    """
    if not prediction_service or not prediction_service.is_loaded:
        raise HTTPException(status_code=503, detail="Prediction service not available")
    
    # Validate file type
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Make prediction
        result = prediction_service.predict(tmp_path)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('error', 'Prediction failed'))
        
        # Get recommendations
        recommendations = prediction_service.get_recommendations(result['predicted_class'])
        
        return PredictionResponse(
            success=True,
            predicted_class=result['predicted_class'],
            crop_type=result['crop_type'],
            disease_status=result['disease_status'],
            confidence=result['confidence'],
            is_healthy=result['is_healthy'],
            top_3_predictions=result['top_3_predictions'],
            recommendation=recommendations['recommendation'],
            urgency=recommendations['urgency']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict-batch", response_model=List[PredictionResponse])
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    Predict crop diseases from multiple uploaded images
    
    - **files**: List of image files (jpg, jpeg, png)
    """
    if not prediction_service or not prediction_service.is_loaded:
        raise HTTPException(status_code=503, detail="Prediction service not available")
    
    results = []
    temp_files = []
    
    try:
        # Process each file
        for file in files:
            # Validate file type
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in [".jpg", ".jpeg", ".png"]:
                continue
            
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                temp_files.append(tmp_file.name)
            
            # Make prediction
            result = prediction_service.predict(tmp_file.name)
            
            if result.get('success'):
                recommendations = prediction_service.get_recommendations(result['predicted_class'])
                
                results.append(PredictionResponse(
                    success=True,
                    predicted_class=result['predicted_class'],
                    crop_type=result['crop_type'],
                    disease_status=result['disease_status'],
                    confidence=result['confidence'],
                    is_healthy=result['is_healthy'],
                    top_3_predictions=result['top_3_predictions'],
                    recommendation=recommendations['recommendation'],
                    urgency=recommendations['urgency']
                ))
        
        # Clean up temporary files
        for tmp_path in temp_files:
            os.unlink(tmp_path)
        
        return results
        
    except Exception as e:
        # Clean up on error
        for tmp_path in temp_files:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/classes")
async def get_disease_classes():
    """Get list of all supported disease classes"""
    from config import DISEASE_CLASSES
    return {
        "total_classes": len(DISEASE_CLASSES),
        "classes": DISEASE_CLASSES
    }


@app.get("/recommendations/{disease_class}")
async def get_recommendations(disease_class: str):
    """Get treatment recommendations for a specific disease"""
    if not prediction_service:
        raise HTTPException(status_code=503, detail="Service not available")
    
    recommendations = prediction_service.get_recommendations(disease_class)
    return recommendations


if __name__ == "__main__":
    import uvicorn
    
    print("Starting Crop Disease Detection API Server...")
    print(f"Host: {API_HOST}")
    print(f"Port: {API_PORT}")
    print(f"API Docs: http://localhost:{API_PORT}/docs")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT
    )
