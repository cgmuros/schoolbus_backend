from fastapi import FastAPI
from db.database import engine
import models
from routers import auth
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)