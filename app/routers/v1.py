import os
from fastapi import APIRouter,FastAPI,File,HTTPException,UploadFile,Request,Depends
from keras.models import load_model
from config import settings
from starlette.middleware.base import BaseHTTPMiddleware
from utils.image_utils import prep,get_top

router = APIRouter(prefix='/V1',tags=['V1'])
app = FastAPI()

model = None
def get_model():
    global model
    if model is None:
        model = load_model(settings.v1_path)
    return model




async def check_key(request:Request,call_next):
    api_key = request.headers.get('X-API-Key')
    if api_key != settings.api_key:
        raise HTTPException(status_code=401,detail='UnAuthorized or Wrong API Key')
    return await call_next(request)

app.include_router(router)

@router.post('/predict')
async def predict(file:UploadFile = File(...),_:None = Depends(check_key)):
    try:
        img = prep((await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400,detail=f'Image Dimension Are Not Compatible: {e}')
    try:
        top_3 = get_top(img,get_model(),3,settings.confidence_threshold)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Prediction Failed :{e}')
    return {'Predictions':top_3}