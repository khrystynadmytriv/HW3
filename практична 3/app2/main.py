import requests
import os
from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from contextlib import asynccontextmanager

APP1_URL = os.getenv("APP1_URL", "http://app1:8000")

async def call_app1():
    try:
        response = requests.get(f"{APP1_URL}/")
        print(f"Response from app1: {response.json()}")
    except Exception as e:
        print(f"Error calling app1: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        call_app1,
        trigger=IntervalTrigger(seconds=10),
        max_instances=1
    )
    scheduler.start()
    
    yield
    
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "This is app2, which calls app1 every 10 seconds"}

@app.get("/health")
def health_check():
    try:
        response = requests.get(f"{APP1_URL}/health", timeout=2)
        return {
            "app2": "running",
            "app1_status": response.status_code
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"App1 unavailable: {str(e)}"
        )