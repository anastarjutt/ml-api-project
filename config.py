import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
load_dotenv()
class appconfig(BaseSettings):
    v1_path:str =  Field('app/models/v1.h5',env='MODEL_PATH_V1')
    v2_path:str =  Field('app/models/v2.h5',env='MODEL_PATH_V2')
    api_key:str =  Field(...,env='API_KEY')
    environment:str = Field('development',env='ENVIRONMENT')
    confidence_threshold:float =  Field(0.2,env='CONFIDENCE_THRESHOLD')
    running_in_docker:bool =     Field(True,env='RUNNING_IN_DOCKER')
    model_config = {
        'env_file':'.env'
    }
settings = appconfig()