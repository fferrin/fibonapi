from fastapi import FastAPI, HTTPException

from .fibonacci import FibonacciService
from pydantic import BaseModel
from typing import Any, List


class Meta(BaseModel):
    page: int
    per_page: int
    total: int


class ResponseListModel(BaseModel):
    data: List[Any]
    metadata: Meta


class FibonacciNumber(BaseModel):
    number: int
    value: int


class ResponseModel(BaseModel):
    data: Any


app = FastAPI()
fibo = FibonacciService()


@app.get("/api/fibonacci/{n}", response_model=ResponseModel)
async def fibonacci_by_number(n: int):
    if n < 0:
        raise HTTPException(
            status_code=400, detail=f"Number must be non negative. Received: {n}"
        )

    return ResponseModel(
        data=FibonacciNumber(
            number=n,
            value=fibo.by_number(int(n)),
        ),
    )


@app.get("/api/fibonacci/{from_}/to/{to}")
async def fibonacci_by_range(from_, to):
    return {"data": {"value": fibo.by_range(int(from_), int(to))}}


@app.post("/api/fibonacci/{n}/blacklist", status_code=204)
async def fibonacci_blacklist_by_number(n):
    fibo.blacklist_by_number(n)
    return


@app.post("/api/fibonacci/{n}/whitelist", status_code=204)
async def fibonacci_whitelist_by_number(n):
    fibo.whitelist_by_number(n)
    return
