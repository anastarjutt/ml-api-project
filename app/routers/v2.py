import os

from fastapi import FastAPI,APIRouter,File,UploadFile,HTTPException,Request,Depends
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings
from keras.models import load_model
from utils.image_utils import prep,get_top

app = FastAPI()
router = APIRouter(prefix='/V2',tags=['V2'])

model = None
def get_model():
    global model
    if model is None:
        model = load_model(settings.v2_path)
    return model

async def check_key(request:Request,call_next):
    api_key = request.headers.get('X-API-Key')
    if api_key != settings.api_key:
        raise HTTPException(401,detail='UnAuthorized or Wrong Key')
    return await call_next(request)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=check_key
)
app.include_router(router)

router.post('/predict')
async def predict(file:UploadFile = File(...),_:None = Depends(check_key)):
    try:
        img_data = await file.read()
        img = prep(img_data)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f'Image Dimension Are Not Compatible: {e}')
    try:
        preds = get_top(img,get_model(),3,settings.confidence_threshold)
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Prediction Failed: {e}')
    return {'Predictions':preds}
