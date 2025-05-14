from typing import Annotated

from fastapi import FastAPI, Query

from .fibonacci import FibonacciService
from .schemas import (
    FibonacciNumber,
    FibonacciRange,
    FilterParams,
    Metadata,
    NonNegativeInt,
    PaginatedResponseModel,
    ResponseModel,
)


app = FastAPI(
    description="FibonnAPI",
    version="0.0.1",
)
fibo = FibonacciService()


@app.get(
    "/api/fibonacci",
    response_model=PaginatedResponseModel,
    tags=["Fibonacci"],
)
async def fibonacci_list(filter_query: Annotated[FilterParams, Query()]):
    page = filter_query.page
    page_size = filter_query.page_size
    from_ = (page - 1) * page_size
    to = from_ + page_size

    return PaginatedResponseModel(
        data=FibonacciRange(
            values=fibo.by_range(from_, to),
        ),
        metadata=Metadata(
            page=page,
            page_size=page_size,
            next=f"/api/fibonacci/?page={page + 1}&page_size={page_size}",
        ),
    )


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
    response_model=ResponseModel,
    tags=["Fibonacci"],
)
async def fibonacci_by_range(from_: NonNegativeInt, to: NonNegativeInt):
    return ResponseModel(
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
