from fastapi import FastAPI, HTTPException

from .fibonacci import FibonacciService
from pydantic import BaseModel
from typing import Any, List, Optional


class Meta(BaseModel):
    page: int
    per_page: int
    total: int


class ResponseModel(BaseModel):
    data: Any


class ResponseListModel(BaseModel):
    data: Any
    metadata: Optional[Meta] = None


class FibonacciNumber(BaseModel):
    number: int
    value: int


class FibonacciRange(BaseModel):
    values: List[int]


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


@app.get("/api/fibonacci/{from_}/to/{to}", response_model=ResponseListModel)
async def fibonacci_by_range(from_: int, to: int):
    if from_ < 0:
        raise HTTPException(
            status_code=400, detail=f"Number must be non negative. Received: {from_}"
        )
    elif to < 0:
        raise HTTPException(
            status_code=400, detail=f"Number must be non negative. Received: {to}"
        )

    return ResponseListModel(
        data=FibonacciRange(
            values=fibo.by_range(int(from_), int(to)),
        ),
    )


@app.post("/api/fibonacci/{n}/blacklist", status_code=204)
async def fibonacci_blacklist_by_number(n: int):
    if n < 0:
        raise HTTPException(
            status_code=400, detail=f"Number must be non negative. Received: {n}"
        )

    fibo.blacklist_by_number(n)


@app.post("/api/fibonacci/{n}/whitelist", status_code=204)
async def fibonacci_whitelist_by_number(n: int):
    if n < 0:
        raise HTTPException(
            status_code=400, detail=f"Number must be non negative. Received: {n}"
        )

    fibo.whitelist_by_number(n)
