from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=5, max_length=55)
    year: int
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Nueva película",
                "overview": "Descripción de la película",
                "year": 2000,
                "rating": 7.0,
                "category": "Comedia",
            }
        }
