import secrets

import fastapi
import fastapi.security

from src.core import settings


api_key_header = fastapi.security.APIKeyHeader(
    name="X-API-KEY",
    auto_error=False,
)


class V1Dependencies:
    def __init__(self, config: settings.APISettings):
        self._config = config

    async def authenticate(self, x_api_key: str = fastapi.Depends(api_key_header)):
        if x_api_key is None or not secrets.compare_digest(x_api_key, self._config.system.x_api_key):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="X-API-KEY incorrect",
            )
