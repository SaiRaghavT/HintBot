from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.run import router as run_router


app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    chat_router,
    prefix="/api",
)

app.include_router(
    run_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "AI Chatbot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }