from fastapi import FastAPI
from fastapi import Request

from fastapi.responses import JSONResponse

from core.config import settings
from core.middleware import autenticador

from api.v1.api import api_router

app = FastAPI(title='Person_Location_Data')

# Middleware
@app.middleware('http')
async def intermediador(request: Request, call_next):
    return await call_next(request) if autenticador(request) else JSONResponse(
                    status_code=403, content={'msg': 'Authentication failed'})

# /api/v1/location
app.include_router(api_router, prefix=settings.API_V1_STR)

# if __name__ == '__main__':
#     import uvicorn

#     uvicorn.run(
#         'main:app', host='0.0.0.0', port=8000,
#         log_level='info', reload=True
#     )
