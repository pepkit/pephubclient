from pydantic import BaseModel


class JWTDataResponse(BaseModel):
    jwt_token: str


class ClientData(BaseModel):
    client_id: str
