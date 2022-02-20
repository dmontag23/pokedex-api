from pydantic import BaseModel


class Health(BaseModel):
    status: str

    class Config:
        schema_extra = {
            "example": {
                "status": "ok",
            }
        }
