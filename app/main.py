from fastapi import FastAPI

from .fibonacci import FibonacciService
from .schemas import (
    FibonacciIndex,
    FibonacciNumber,
    FibonacciRange,
    Meta,
    NonNegativeInt,
    ResponseListModel,
    ResponseModel,
)


app = FastAPI(
    description="FibonnAPI",
    version="0.0.1",
)
fibo = FibonacciService()


@app.get(
    "/api/fibonacci/{n}",
    response_model=ResponseModel,
    tags=["Fibonacci"],
)
async def fibonacci_by_number(n: NonNegativeInt):
    return ResponseModel(
        data=FibonacciNumber(
            number=n,
            value=fibo.by_number(int(n)),
        ),
    )


@app.get(
    "/api/fibonacci/{from_}/to/{to}",
    response_model=ResponseListModel,
    tags=["Fibonacci"],
)
async def fibonacci_by_range(from_: NonNegativeInt, to: NonNegativeInt):
    return ResponseListModel(
        data=FibonacciRange(
            values=fibo.by_range(int(from_), int(to)),
        ),
    )


@app.post(
    "/api/fibonacci/{n}/blacklist",
    status_code=204,
    tags=["Access Control"],
)
async def fibonacci_blacklist_by_number(n: NonNegativeInt):
    fibo.blacklist_by_number(n)


@app.post(
    "/api/fibonacci/{n}/whitelist",
    status_code=204,
    tags=["Access Control"],
)
async def fibonacci_whitelist_by_number(n: NonNegativeInt):
    fibo.whitelist_by_number(n)
