from typing import Optional

from pydantic import BaseModel


class VerificationCodesResponseModel(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: Optional[int]
    interval: Optional[int]


class AccessTokenResponseModel(BaseModel):
    access_token: str
    scope: Optional[str]
    token_type: Optional[str]
