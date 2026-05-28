from app.core.database import Base, engine
import app.modules.urls.models  # noqa: F401 — registers models with Base

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
