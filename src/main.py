from core import app_settings, get_production_app

import uvicorn


app = get_production_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port,
        reload=True,
    )
