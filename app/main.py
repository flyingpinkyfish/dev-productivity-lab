from fastapi import FastAPI

app = FastAPI()
VERSION = "0.1.0"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}

@app.get("/")
def root():
    return {"message": "dev-productivity-lab"}

@app.get("/version")
def version():
    return {"version": VERSION}
