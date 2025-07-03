from fastapi import Depends, Request, HTTPException, status
from firebase_admin import auth



async def get_current_user(request: Request):
    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authorization header missing"
        )
    
    # Remove 'Bearer ' prefix if present
    jwt = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header
    
    try:
        user = auth.verify_id_token(jwt)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Invalid or expired token: {str(e)}"
        )