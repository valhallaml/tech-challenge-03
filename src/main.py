import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from api.router import api_router
# from core.database import Base, engine
from core.configs import settings
from dotenv import load_dotenv

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Football API",
    description = "Football Data Collection API",
    summary = '',
    version = '1.0.0'
)

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("src/home.html") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    load_dotenv()
    environment = os.getenv('ENVIRONMENT', 'development')
    is_dev = environment == 'development'
    uvicorn.run(app = 'main:app', host = "0.0.0.0", port = 8000, reload = is_dev)
