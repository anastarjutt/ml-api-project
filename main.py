import os,logging
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import v1,v2,upload_router
from fastapi.responses import JSONResponse

app = FastAPI(
    title='Dual Model APi',
    description='Dual Model API Trained on 17 Flowers',
    version='1.0.0',
    license_info={'name':'MIT'},
    contact={'Name':'Waleed','Email':'@gmail.com'}
)

app.add_middleware(
    CORSMiddleware,
    allow_headers=['*'],
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True
)
app.include_router(v1.router)
app.include_router(v2.router)
app.include_router(upload_router.router)

@app.get('/health')
def get_health():
    return {'Status':'OK'}
@app.exception_handler(Exception)
async def global_exception_handler(request:Request,exc:Exception):
    logging.error(f'UnHandled Error: {exc}')
    return JSONResponse(status_code=500,content={'Detail':'Internal Server Error'})
