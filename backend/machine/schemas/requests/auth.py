from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
    
class VerifyEmailRequest(BaseModel):
    email: str
    code: str