from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl 

class ErrorResponse(BaseModel):
    detail: str