from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.base import Sender, SessionStatus


# ---------- Session Schemas ----------

class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    user_identifier: str = Field(..., min_length=1, max_length=100)


class SessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    last_activity_at: datetime
    status: SessionStatus
    user_identifier: str

    class Config:
        from_attributes = True


# ---------- Message Schemas ----------

class MessageCreate(BaseModel):
    sender: Sender
    content: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    id: int
    session_id: int
    sender: Sender
    content: str
    created_at: datetime
    order: int

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]


class SubmitMessageResponse(BaseModel):
    user_message: MessageResponse
    ai_message: MessageResponse