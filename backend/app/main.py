from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import password, social, learning, awareness, stats

app = FastAPI(title="Cybersecurity Training Platform", version="1.0.0")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(password.router, prefix="/api/password", tags=["password"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(awareness.router, prefix="/api/awareness", tags=["awareness"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cybersecurity Training Platform API"}
