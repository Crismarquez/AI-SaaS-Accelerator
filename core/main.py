from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Base, engine, settings
from .routers import health, users
from .utils.firebase import firebase_app


# Create database tables on startup (simple approach; replace with migrations in prod)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Core Backend", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

# Initialize Firebase Admin on startup
@app.on_event("startup")
def _startup():
    # Lazy init
    firebase_app()


app.include_router(health.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"service": "core-backend", "status": "ok"}


