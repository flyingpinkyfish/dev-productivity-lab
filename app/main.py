import logging

from fastapi import FastAPI, HTTPException, Query, Request

app = FastAPI()
logger = logging.getLogger("uvicorn.error")



@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response

VERSION = "0.1.0"

@app.get("/first_char")
def first_char(text: str):
    if text == "":
        raise HTTPException(status_code=400, detail="Text must not be empty")
    return {"result": text[0]}

@app.get("/square")
def square_number(n: int = Query(..., description="The number to square")):
    return {"result": n ** 2}

@app.get("/cube")
def cube_number(n: int = Query(..., description="The number to cube")):
    return {"result": n * n * n}

@app.get("/vowels")
def count_vowels(text: str = Query(..., description="The text to count vowels from")):
    vowels = "aeiouAEIOU"
    vowel_count = sum(1 for char in text if char in vowels)
    
    return {"result": vowel_count}

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

@app.get("/concatenate")
def concatenate(a:str, b:str):
    return {"result": a+b}
