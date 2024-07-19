from fastapi import FastAPI

from distribuidora.routers import distribuidora_router
from shared.database import Base, engine

app = FastAPI()


#@app.on_event("startup")
#async def startup_event():
    #Base.metadata.drop_all(bind=engine)
    #Base.metadata.create_all(bind=engine)



app.include_router(distribuidora_router.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
