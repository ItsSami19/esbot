from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field

# test-entity for user sessions; for exercise 4.2, pls modify this file to add more fields as needed...
class UserSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)