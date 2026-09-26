# Authentication Plan

## Overview
LegiSim will use OpenID Connect (OIDC) through Keycloak for robust enterprise/government identity management. The FastAPI backend will serve as a Resource Server, verifying JWTs.

**Subagents Required**: 
- `auth-specialist` (Keycloak configuration & JWT validation logic)

## Flow
1. **Frontend**: Next.js (Auth.js) initiates OAuth2 flow with Keycloak.
2. **Keycloak**: Authenticates user, returns Access Token (JWT) to Next.js.
3. **Frontend**: Next.js attaches the JWT to the `Authorization: Bearer <token>` header for all API calls to FastAPI.
4. **Backend**: FastAPI validates the token signature using Keycloak's public keys (JWKS).

## Roles and RBAC
Keycloak will define roles:
- `officer` (Create simulations, edit settings)
- `analyst` (View and analyze runs)
- `admin` (System management)

## FastAPI Implementation

```python
# app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import requests

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://auth.legisim.com/realms/legisim/protocol/openid-connect/auth",
    tokenUrl="https://auth.legisim.com/realms/legisim/protocol/openid-connect/token"
)

JWKS_URL = "https://auth.legisim.com/realms/legisim/protocol/openid-connect/certs"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        jwks = requests.get(JWKS_URL).json()
        # Decode and validate using python-jose
        payload = jwt.decode(token, jwks, algorithms=["RS256"], audience="legisim-backend")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## Guest Mode
For shared read-only links:
- Runs can have a `share_token` (UUID).
- Specific endpoints (e.g., `GET /api/runs/{id}/public?token=...`) will bypass `get_current_user` and instead validate the `share_token`.
