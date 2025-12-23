import json
from typing import Dict
from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import FastAPI
from shared_model import DIDRegistryRegisterRequest, DIDRegistryRegisterResponse, DIDRegistryResolveResponse, Demo, IPFSStoreRequest, IPFSStoreResponse, IPFSRetrieveResponse
from utils import *

app = FastAPI()

app.post("/")
def index():
    pass