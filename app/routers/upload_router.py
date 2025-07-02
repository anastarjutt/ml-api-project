from fastapi import APIRouter,UploadFile,File,HTTPException
from fastapi.responses import JSONResponse
from config import settings
from PIL import Image
import numpy as np
import io
from app.routers.v1 import get_model
router = APIRouter()
model = get_model()

class_names = [
    'daffodil','snowdrop','lily_valley','bluebell','crocus','iris','tigerlily','tulip','fritillary',
    'sunflower','daisy','colts_foot','dandelion','cowslip','buttercup','windflower','pansy'
]

@router.post('/upload')
async def upload(file:UploadFile = File(...)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400,detail='Invalid File Type,')
        data = await file.read()
        img = Image.open(io.BytesIO(data)).convert('RGB').resize((224,224))
        img = np.array(img,dtype=np.float32)/255.0
        img = np.expand_dims(img,axis=0)
        preds = model.predict(img)[0]
        idx = np.argmax(preds)
        confi = float(np.max(preds))
        label = class_names[idx]
        return {'Prediction':label,'Confidence':confi}
    except Exception as e:
        raise HTTPException(status_code=500,detail='Prediction Failed')
    