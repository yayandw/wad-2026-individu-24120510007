from fastapi import FastAPI

from app.routes import router as menu_router

app = FastAPI(title="The Build API")
app.include_router(menu_router)


@app.get("/health")
def health():
    return {"status": "ok"}
