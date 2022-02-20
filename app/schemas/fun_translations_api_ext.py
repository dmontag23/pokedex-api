from pydantic import BaseModel


class TranslationsExtCreate(BaseModel):
    text: str


class Contents(BaseModel):
    translated: str


class Total(BaseModel):
    total: str


class TranslationsExtResponse(BaseModel):
    success: Total
    contents: Contents
