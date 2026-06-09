from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field as PydanticField

from sqlalchemy import JSON
from sqlmodel import Column, Date, Field, SQLModel

Platform = Literal["PC", "PS3", "PS4", "PS5", "Switch", "One", "WiiU"]


class VideoGameBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    release_date: date = Field(sa_column=Column(Date))
    ratings: int = Field(nullable=True, le=20, ge=0)
    studio: str = Field(nullable=True, max_length=100)
    platform: List[str] = Field(sa_column=Column(JSON, nullable=False))


class VideoGameCreate(SQLModel):
    name: str = Field(max_length=100, min_length=1)
    release_date: date
    ratings: int = Field(le=20, ge=0)
    studio: str = Field(max_length=100)
    platform: List[Platform]


class VideoGamePatch(SQLModel):
    name: Optional[str] = Field(default=None, max_length=100, min_length=1)
    release_date: Optional[date] = None
    ratings: Optional[int] = Field(default=None, le=20, ge=0)
    studio: Optional[str] = Field(default=None, max_length=100)
    platform: Optional[List[Platform]] = None


class VideoGameFilters(BaseModel):
    name: Optional[str] = None
    studio: Optional[str] = None
    platform: Optional[List[Platform]] = None
    release_date_from: Optional[date] = None
    release_date_to: Optional[date] = None
    min_ratings: Optional[int] = PydanticField(default=None, ge=0, le=20)
    max_ratings: Optional[int] = PydanticField(default=None, ge=0, le=20)
    limit: int = PydanticField(default=20, ge=1, le=100)
    offset: int = PydanticField(default=0, ge=0)
