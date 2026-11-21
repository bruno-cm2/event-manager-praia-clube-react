from fastapi import FastAPI
import auth
from logs import LogLevels, configure_logging

configure_logging(level=LogLevels.INFO)

app = FastAPI()

app.include_router(auth.router)