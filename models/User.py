from sqlmodel import SQLModel,Field
from typing import Optional

class User(SQLModel):
    username: str
    email: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    disabled: Optional[bool] = Field(default=False)
