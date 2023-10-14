from core import get_production_app, settings

import uvicorn


app = get_production_app()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )
