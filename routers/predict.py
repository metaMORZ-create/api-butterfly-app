# routers/predict.py

from fastapi import APIRouter, UploadFile, HTTPException
from model.inference import predict_image

router = APIRouter()

@router.post("/predict", tags=["classification"])
async def classify_image(file: UploadFile):
    """
    Nimmt ein Bild entgegen (JPEG/PNG/WebP) und gibt die vorhergesagte Schmetterlingsart zurück.
    """
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=415, detail="Unsupported media type")
    image_bytes = await file.read()
    try:
        species = predict_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    return {"filename": file.filename, "species": species}
