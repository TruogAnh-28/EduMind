from uuid import UUID
from pydantic import BaseModel

class WelcomeMessageRequest(BaseModel):
    student_id: UUID