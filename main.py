from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from distribuidora.routers import distribuidora_router
from shared.database import Encomenda, Base, engine, SessionLocal
import logging

app = FastAPI()

# Configuração do logger
logger = logging.getLogger("uvicorn")
tz_brasilia = timezone(timedelta(hours=-3))

def atualizar_status_encomendas():
    try:
        db = SessionLocal()
        agora = datetime.now(timezone.utc)
        encomendas = db.query(Encomenda).filter(Encomenda.prazo_entrega < agora,
                                                Encomenda.status_encomenda == True).all()
        for encomenda in encomendas:
            encomenda.status_encomenda = False
        db.commit()
    except Exception as e:
        print(f"Erro ao atualizar status das encomendas: {e}")
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
