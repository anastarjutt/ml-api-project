import os,io
import numpy as np
from PIL import Image
from fastapi import HTTPException

class_names = [
    'daffodil','snowdrop','lily_valley','bluebell','crocus','iris','tigerlily','tulip','fritillary',
    'sunflower','daisy','colts_foot','dandelion','cowslip','buttercup','windflower','pansy'
]

async def prep(file,trg_size=(224,224)):
    try:
        data = await file.read()
        img = Image.open(io.BytesIO(data)).convert('RGB').resize(trg_size)
        img = np.array(img,dtype=np.float32)/255.0
        img = np.expand_dims(img,axis=0)
    except Exception as e:
        HTTPException(status_code=400,detail=f'Image PreProcessing Failed: {e}')
    return img
def get_top(img,model,top_k,threshold):
    preds = model.predict(img)[0]
    top_idx = np.argsort(preds)[-top_k:][::-1]
    results = [{f'Top {rank + 1} Prediction':int(i),'Label':class_names[i],'Confidence':preds[i]} for rank,i in enumerate(top_idx) if preds[i] >= threshold]
    return results

