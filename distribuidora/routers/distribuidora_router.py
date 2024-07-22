from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from distribuidora.models.distribuidora_models import EncomendaRequest, EncomendaResponse, ClienteRequest, \
    ClienteResponse, MotoristaRequest, MotoristaResponse, VeiculoRequest, VeiculoResponse
from shared.database import Encomenda, Cliente, Motorista, Veiculo, Fornecedor
from shared.dependencies import get_db
import logging
from shared.database import SessionLocal
from distribuidora.models.fornecedor_models import FornecedorRequest, FornecedorResponse




router = APIRouter()
tz_brasilia = timezone(timedelta(hours=-3))
logger = logging.getLogger("uvicorn")


def estimar_prazo_entrega(endereco: str) -> datetime:
    localidades_1h = ["centro", "brotas", "costa azul", "caminho das arvores",
                      "cidade alta", "pernambués", "boca do rio"]
    localidades_40min = ["ondina", "federação", "barra", "pituba",
                         "amaralina", "rio vermelho", "graça"]

    if endereco.lower() in localidades_1h:
        return datetime.now(tz=tz_brasilia) + timedelta(hours=1)
    elif endereco.lower() in localidades_40min:
        return datetime.now(tz=tz_brasilia) + timedelta(minutes=40)
    else:
        return datetime.now(tz=tz_brasilia) + timedelta(hours=2)


@router.get("/encomendas", response_model=list[EncomendaResponse])
def listar_encomendas(db: Session = Depends(get_db)):
    encomendas = db.query(Encomenda).all()
    return encomendas


@router.post("/conta-do-cliente", response_model=ClienteResponse, status_code=201)
def criar_conta(conta: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    try:
        logger.debug(f"Tentando criar cliente: {conta}")

        if db.query(Cliente).filter(Cliente.cpf == conta.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")

        novo_cliente = Cliente(
            nome=conta.nome,
            idade=conta.idade,
            endereco=conta.endereco,
            telefone=conta.telefone,
            status_atividade=True,
            cpf=conta.cpf,
            data_registro=datetime.now(tz=tz_brasilia)
        )
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        logger.debug(f"Cliente criado: {novo_cliente}")
        return novo_cliente
    except Exception as e:
        logger.error(f"Erro ao criar cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")


@router.post("/criar-encomenda", response_model=EncomendaResponse, status_code=201)
def criar_encomenda(encomenda: EncomendaRequest, db: Session = Depends(get_db)) -> EncomendaResponse:
    try:
        logger.debug(f"Tentando criar encomenda: {encomenda}")

        cliente = db.query(Cliente).filter(Cliente.nome == encomenda.cliente).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado.")

        motorista = db.query(Motorista).filter(Motorista.status_ativo == True).first()
        if not motorista:
            raise HTTPException(status_code=404, detail="Nenhum motorista disponível.")

        veiculo = db.query(Veiculo).filter(Veiculo.motorista_id == motorista.id, Veiculo.status_ativo == True).first()
        if not veiculo:
            raise HTTPException(status_code=404, detail="Nenhum veículo disponível para o motorista.")

        prazo_entrega_estimado = estimar_prazo_entrega(cliente.endereco)
        nova_encomenda = Encomenda(
            cliente_id=cliente.id,
            quantidade=encomenda.quantidade,
            descricao=encomenda.descricao,
            prazo_entrega=prazo_entrega_estimado,
            data_pedido=datetime.now(tz=tz_brasilia),
            status_encomenda=encomenda.status_encomenda,
            motorista_id=motorista.id,
            veiculo_id=veiculo.id
        )
        db.add(nova_encomenda)

        motorista.status_ativo = False
        veiculo.status_ativo = False

        db.commit()
        db.refresh(nova_encomenda)
        logger.debug(f"Encomenda criada: {nova_encomenda}")

        return EncomendaResponse(
            id=nova_encomenda.id,
            cliente_id=nova_encomenda.cliente_id,
            quantidade=nova_encomenda.quantidade,
            descricao=nova_encomenda.descricao,
            prazo_entrega=nova_encomenda.prazo_entrega,
            data_pedido=nova_encomenda.data_pedido,
            status_encomenda=nova_encomenda.status_encomenda,
            motorista_id=nova_encomenda.motorista_id,
            veiculo_id=nova_encomenda.veiculo_id
        )
    except HTTPException as e:
        logger.error(f"Erro HTTP ao criar encomenda: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Erro inesperado ao criar encomenda: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")



@router.get("/clientes/{cliente_id}/encomendas", response_model=list[EncomendaResponse])
def listar_encomendas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    encomendas = db.query(Encomenda).filter(Encomenda.cliente_id == cliente_id).all()
    if not encomendas:
        raise HTTPException(status_code=404, detail="Cliente não encontrado ou sem encomendas.")
    return encomendas


@router.post("/conta-do-motorista", response_model=MotoristaResponse, status_code=201)
def criar_motorista(motorista: MotoristaRequest, db: Session = Depends(get_db)) -> MotoristaResponse:
    try:
        logger.debug(f"Tentando criar motorista: {motorista}")

        novo_motorista = Motorista(
            nome=motorista.nome,
            idade=motorista.idade,
            telefone=motorista.telefone,
            endereco=motorista.endereco,
            email=motorista.email,
            status_ativo=True,
            cpf=motorista.cpf
        )
        db.add(novo_motorista)
        db.commit()
        db.refresh(novo_motorista)

        veiculo = Veiculo(
            motorista_id=novo_motorista.id,
            marca=motorista.veiculo.marca,
            modelo=motorista.veiculo.modelo,
            ano=motorista.veiculo.ano,
            status_ativo=motorista.veiculo.status_ativo
        )
        db.add(veiculo)
        db.commit()
        db.refresh(veiculo)

        logger.debug(f"Motorista e veículo criados: {novo_motorista}, {veiculo}")
        return MotoristaResponse(
            id=novo_motorista.id,
            idade=novo_motorista.idade,
            nome=novo_motorista.nome,
            telefone=novo_motorista.telefone,
            endereco=novo_motorista.endereco,
            email=novo_motorista.email,
            status_ativo=novo_motorista.status_ativo,
            cpf=novo_motorista.cpf
        )
    except Exception as e:
        logger.error(f"Erro ao criar motorista: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")



@router.get("/motoristas", response_model=list[MotoristaResponse])
def listar_motoristas(db: Session = Depends(get_db)):
    motoristas = db.query(Motorista).all()
    return motoristas


@router.get("/veiculos", response_model=list[VeiculoResponse])
def listar_veiculos(db: Session = Depends(get_db)):
    veiculos = db.query(Veiculo).all()
    return veiculos

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

@router.post("/criar-fornecedor", response_model=FornecedorResponse)
def criar_fornecedor(fornecedor: FornecedorRequest, db: Session = Depends(get_db)) -> FornecedorResponse:
    try:
        novo_fornecedor = Fornecedor(
            nome=fornecedor.nome,
            cnpj=fornecedor.cnpj,
            endereco=fornecedor.endereco,
            email=fornecedor.email,
            telefone=fornecedor.telefone,
            status_ativo=True
        )
        db.add(novo_fornecedor)
        db.commit()
        db.refresh(novo_fornecedor)

        return FornecedorResponse(
            id=novo_fornecedor.id,
            nome=novo_fornecedor.nome,
            endereco=novo_fornecedor.endereco,
            email=novo_fornecedor.email,
            telefone=novo_fornecedor.telefone,
            cnpj=novo_fornecedor.cnpj,
            status_ativo=novo_fornecedor.status_ativo
        )
    except Exception as e:
        logger.error(f"Erro ao criar fornecedor: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")

@router.get("/listar-fornecedores", response_model=list[FornecedorResponse])
def listar_fornecedores(db: Session = Depends(get_db)):
    fornecedores = db.query(Fornecedor).all()
    return fornecedores