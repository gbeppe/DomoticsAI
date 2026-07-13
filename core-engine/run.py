from domoticsai_core.app import app
from domoticsai_core.config import Settings
import uvicorn

if __name__ == "__main__":
    settings = Settings.from_env()
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
    )
