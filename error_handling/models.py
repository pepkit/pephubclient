from pydantic import BaseModel


class GithubErrorModel(BaseModel):
    error: str
    error_description: str
