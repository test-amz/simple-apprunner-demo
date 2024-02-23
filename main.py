#!/usr/bin/env python3

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from os import getenv

import boto3
import requests
from requests_aws4auth import AWS4Auth

host = 'https://search-test-sm-m5zxhdizelbznif3vjpfra56oe.us-east-1.es.amazonaws.com' 
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

path = '/_search' # the OpenSearch API endpoint
url = host + path

headers = {"Content-Type": "application/json"}


app = FastAPI(
    title="App Runner Demo Service",
    description="Demo API",
    version="1.0.0",
)

DEMO_ENV_VAR = getenv('DEMO_ENV_VAR')

@app.get("/health")
def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": "Healthy"})

@app.get("/")
def root():
    msg = "Hello from app runner!"
    if DEMO_ENV_VAR:
        msg += f" You set this environment variable: {DEMO_ENV_VAR}"
        r = requests.get(url, auth=awsauth, headers=headers)
    return JSONResponse(status_code=status.HTTP_200_OK, content=r)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
