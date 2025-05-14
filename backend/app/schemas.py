from fastapi import Path

from pydantic import BaseModel, Field
from typing import Annotated, Any, List, Optional


NonNegativeInt = Annotated[int, Path(ge=0)]


class Metadata(BaseModel):
    page: int
    page_size: int
    next: Optional[str] = None


class FilterParams(BaseModel):
    page: int = Field(1, gt=0, le=25)
    page_size: int = Field(100, gt=0, le=100)


class ResponseModel(BaseModel):
    data: Any


class PaginatedResponseModel(BaseModel):
    data: Any
    metadata: Metadata


class FibonacciIndex(BaseModel):
    number: NonNegativeInt


class FibonacciNumber(BaseModel):
    number: int
    value: int


class FibonacciRange(BaseModel):
    values: List[int]
