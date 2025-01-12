from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

app = FastAPI(title="Reports Service")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #TODO: Change this to the API Gateway URL
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Lambda handler
handler = Mangum(app)
