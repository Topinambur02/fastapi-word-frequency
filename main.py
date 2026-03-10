from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import settings
from APIRouter import api_router

import uvicorn

app = FastAPI()


app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


def main():
    uvicorn.run(app="main:app", host=settings.HOST, port=settings.PORT, reload=True)


if __name__ == "__main__":
    main()
