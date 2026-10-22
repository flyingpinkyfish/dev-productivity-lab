from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
VERSION = "0.1.0"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/add")
def add(a: int = Query(..., le=1_000_000), b: int = Query(..., le=1_000_000)):
    return {"result": a + b}

@app.get("/subtract")
def subtract(a: int, b: int):
    return {"result": a - b}

@app.get("/multiply")
def multiply(a: int, b: int):
    return {"result": a * b}

@app.get("/")
def root():
    return {"message": "dev-productivity-lab"}

@app.get("/version")
def version():
    return {"version": VERSION}

@app.get("/divide")
def divide(a: int, b:int):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}    

@app.get("/echo")
def echo(text: str):
    return {"text": text}
