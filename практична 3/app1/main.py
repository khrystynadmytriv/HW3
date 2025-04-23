from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, I'm inside a container!"}

@app.get("/health")
def health():
    return {"status": "OK"}