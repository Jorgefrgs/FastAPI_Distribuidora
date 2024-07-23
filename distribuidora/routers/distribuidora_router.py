from datetime import timedelta, timezone

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from distribuidora.models.distribuidora_models import *
from distribuidora.models.fornecedor_models import FornecedorRequest, FornecedorResponse
from shared.database import Encomenda, Cliente, Motorista, Veiculo, Fornecedor, Pagamento, Produto, Categoria
from shared.dependencies import get_db
from distribuidora.models.veiculo_models import VeiculoRequest, VeiculoResponse
from typing import List

router = APIRouter()
tz_brasilia = timezone(timedelta(hours=-3))


@router.post("/criar-clientes/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteRequest, db: Session = Depends(get_db)):
    db_cliente = Cliente(
        nome=cliente.nome,
        idade=cliente.idade,
        endereco=cliente.endereco,
        telefone=cliente.telefone,
        email=cliente.email,
        status_atividade=True,
        cpf=cliente.cpf,
        data_registro=datetime.now(tz=tz_brasilia)
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/listar-clientes/", response_model=List[ClienteResponse])
def list_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return clientes

@router.post("/criar-motoristas/", response_model=MotoristaResponse)
def create_motorista(motorista: MotoristaRequest, db: Session = Depends(get_db)):
    db_motorista = Motorista(
        nome=motorista.nome,
        idade=motorista.idade,
        endereco=motorista.endereco,
        telefone=motorista.telefone,
        email=motorista.email,
        status_ativo=True,
        cpf=motorista.cpf
    )
    db.add(db_motorista)
    db.commit()
    db.refresh(db_motorista)

    return db_motorista

@router.get("/listar-motoristas/", response_model=List[MotoristaResponse])
def list_motoristas(db: Session = Depends(get_db)):
    motoristas = db.query(Motorista).all()
    return motoristas

@router.post("/criar-encomendas/", response_model=EncomendaResponse)
def create_encomenda(encomenda: EncomendaRequest, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.nome == encomenda.cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    produto_objs = []
    for produto_id in encomenda.produtos:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto com id {produto_id} não encontrado")
        produto_objs.append(produto)

    veiculo_livre = db.query(Veiculo).filter(Veiculo.status_ativo == True).first()
    if not veiculo_livre:
        raise HTTPException(status_code=400, detail="Não há veículos disponíveis no momento")

    veiculo_livre.status_ativo = False
    db.commit()

    motorista = db.query(Motorista).filter(Motorista.id == veiculo_livre.motorista_id).first()
    if not motorista:
        raise HTTPException(status_code=400, detail="Motorista não encontrado para o veículo selecionado")

    # Definindo prazo de entrega como uma semana a partir da data do pedido
    prazo_entrega = datetime.now(tz=tz_brasilia) + timedelta(weeks=1)

    db_encomenda = Encomenda(
        cliente_id=cliente.id,
        quantidade=encomenda.quantidade,
        descricao=encomenda.descricao,
        data_pedido=datetime.now(tz=tz_brasilia),
        prazo_entrega=prazo_entrega,  # Adicionando prazo de entrega
        status_encomenda=encomenda.status_encomenda,
        motorista_id=motorista.id,
        veiculo_id=veiculo_livre.id,
        produtos=produto_objs
    )
    db.add(db_encomenda)
    db.commit()
    db.refresh(db_encomenda)
    return db_encomenda

    cliente = db.query(Cliente).filter(Cliente.nome == encomenda.cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    produto_objs = []
    for produto_id in encomenda.produtos:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto com id {produto_id} não encontrado")
        produto_objs.append(produto)

    veiculo_livre = db.query(Veiculo).filter(Veiculo.status_ativo == True).first()
    if not veiculo_livre:
        raise HTTPException(status_code=400, detail="Não há veículos disponíveis no momento")

    veiculo_livre.status_ativo = False
    db.commit()

    motorista = db.query(Motorista).filter(Motorista.id == veiculo_livre.motorista_id).first()
    if not motorista:
        raise HTTPException(status_code=400, detail="Motorista não encontrado para o veículo selecionado")

    db_encomenda = Encomenda(
        cliente_id=cliente.id,
        quantidade=encomenda.quantidade,
        descricao=encomenda.descricao,
        data_pedido=datetime.now(tz=tz_brasilia),
        status_encomenda=encomenda.status_encomenda,
        motorista_id=motorista.id,
        veiculo_id=veiculo_livre.id,
        produtos=produto_objs
    )
    db.add(db_encomenda)
    db.commit()
    db.refresh(db_encomenda)
    return db_encomenda
@router.get("/listar-encomendas-do-cliente/", response_model=List[EncomendaResponse])
def list_encomendas_by_cliente_email(email: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    encomendas = db.query(Encomenda).filter(Encomenda.cliente_id == cliente.id).all()
    return encomendas

@router.post("/criar-fornecedores/", response_model=FornecedorResponse)
def create_fornecedor(fornecedor: FornecedorRequest, db: Session = Depends(get_db)):
    db_fornecedor = Fornecedor(
        nome=fornecedor.nome,
        endereco=fornecedor.endereco,
        telefone=fornecedor.telefone,
        email=fornecedor.email,
        status_ativo=True,
        cnpj=fornecedor.cnpj
    )
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

@router.get("/listar-fornecedores/", response_model=List[FornecedorResponse])
def list_fornecedores(db: Session = Depends(get_db)):
    fornecedores = db.query(Fornecedor).all()
    return fornecedores

@router.post("/criar-pagamentos/", response_model=PagamentoResponse)
def create_pagamento(pagamento: PagamentoRequest, db: Session = Depends(get_db)):
    db_pagamento = Pagamento(
        encomenda_id=pagamento.encomenda_id,
        valor=pagamento.valor,
        metodo_pagamento=pagamento.metodo_pagamento,
        data_pagamento=datetime.now(tz=tz_brasilia)
    )
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.post("/criar-produtos/", response_model=ProdutoResponse)
def create_produto(produto: ProdutoRequest, db: Session = Depends(get_db)):
    db_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        categoria_id=produto.categoria_id,
        fornecedor_id=produto.fornecedor_id,
        data_criacao=datetime.now(tz=tz_brasilia)
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.get("/listar-produtos/", response_model=List[ProdutoResponse])
def list_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos

@router.post("/criar-categorias/", response_model=CategoriaResponse)
def create_categoria(categoria: CategoriaRequest, db: Session = Depends(get_db)):
    db_categoria = Categoria(
        nome=categoria.nome,
        descricao=categoria.descricao,
        data_criacao=datetime.now(tz=tz_brasilia)
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.post("/criar-veiculos/", response_model=VeiculoResponse)
def create_veiculo(veiculo: VeiculoRequest, db: Session = Depends(get_db)):
    db_veiculo = Veiculo(
        marca=veiculo.marca,
        placa=veiculo.placa,
        modelo=veiculo.modelo,
        ano=veiculo.ano,
        status_ativo=veiculo.status_ativo,
        motorista_id=veiculo.motorista_id
    )
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

@router.get("/listar-veiculos/", response_model=List[VeiculoResponse])
def list_veiculos(db: Session = Depends(get_db)):
    veiculos = db.query(Veiculo).all()
    return veiculos