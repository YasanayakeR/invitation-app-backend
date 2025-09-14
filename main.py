import os
from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.admin_routes import router as admin_router

app = FastAPI(title="User Management API", description="API with admin authentication")

app.include_router(user_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
