from fastapi import FastAPI
from src.api import init_api


app: FastAPI = init_api()
