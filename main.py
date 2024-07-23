import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from distribuidora.routers import distribuidora_router
from shared.database import Encomenda, SessionLocal

app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
tz_brasilia = timezone(timedelta(hours=-3))

def atualizar_status_encomendas():
    try:
        db = SessionLocal()
        agora = datetime.now(tz=tz_brasilia)
        encomendas = db.query(Encomenda).filter(Encomenda.prazo_entrega < agora,
                                                Encomenda.status_encomenda == True).all()
        for encomenda in encomendas:
            encomenda.status_encomenda = False
        db.commit()
    except Exception as e:
        logger.error(f"Erro ao atualizar status das encomendas: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(atualizar_status_encomendas, 'interval', minutes=1)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

app.include_router(distribuidora_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
