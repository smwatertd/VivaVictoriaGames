from core.app_factory import get_production_app
from core.settings import app_settings

import uvicorn


app = get_production_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
