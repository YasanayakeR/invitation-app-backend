from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.services.auth_service import verify_admin_passcode, create_access_token, verify_token

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()

class AdminLogin(BaseModel):
    passcode: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenResponse)
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint that requires passcode"""
    if not verify_admin_passcode(login_data.passcode):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin passcode"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": "admin", "role": "admin"})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to verify admin token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return payload
