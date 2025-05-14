from fastapi import Path

from pydantic import BaseModel
from typing import Annotated, Any, List, Optional


NonNegativeInt = Annotated[int, Path(ge=0)]


class Meta(BaseModel):
    page: int
    per_page: int
    total: int


class ResponseModel(BaseModel):
    data: Any


class ResponseListModel(BaseModel):
    data: Any
    metadata: Optional[Meta] = None


class FibonacciIndex(BaseModel):
    number: NonNegativeInt


class FibonacciNumber(BaseModel):
    number: int
    value: int


class FibonacciRange(BaseModel):
    values: List[int]
