from pydantic import BaseModel
import requests
from config import *
from shared_model import DIDRegistryRegisterRequest, Demo, IPFSStoreRequest, IPFSStoreResponse

endpoint = {
    "reg":"/register",
    "res":"/resolve/",
    "str":"/store",
    "ret":"/retrieve/"
}

def finalizeUrl(key:str, val:str=None):
    part = endpoint[key]
    url = f"{HOST}:{PORT}{part}"
    if val:
        url = url + val
    return url

def register(did, cid, signature=None):
    url = finalizeUrl("reg")
    data = DIDRegistryRegisterRequest(did=did, doc_cid=cid, signature=None)
    req = requests.post(url,data=data.model_dump_json())
    print(req.json())

def resolve(did):
    url = finalizeUrl(key="res", val=did)
    req = requests.get(url)
    print(req.json())

def store(model:BaseModel):
    url = finalizeUrl("str")
    json_model = model.model_dump()
    res = IPFSStoreRequest(document=json_model)
    req = requests.post(url, data=res.model_dump_json())
    print(req.json())

def retrieve(cid):
    url = finalizeUrl(key="ret", val=cid)
    req = requests.get(url)
    print(req.json())

if __name__ == "__main__":
    register("did:dz", cid="dffe")
    resolve("did:dz")
    #a = Demo
    #store(a)
    #retrieve("cid_a3e2a4db6db754e3e4734e0de1b78eb09e3cc3b04a4c37985893969a1b20401b5")