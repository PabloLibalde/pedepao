from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer(auto_error=False)

def admin_guard(token: HTTPAuthorizationCredentials | None = Depends(bearer)):
    # Placeholder simples (trocar por JWT real)
    if not token or token.credentials != "admin-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
