from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:862100@localhost/db_fastapi_distribuidora"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

encomenda_produto_association = Table(
    'encomenda_produto',
    Base.metadata,
    Column('encomenda_id', Integer, ForeignKey('encomendas.id')),
    Column('produto_id', Integer, ForeignKey('produtos.id'))
)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String, unique=True, index=True)
    status_atividade = Column(Boolean, default=True)
    cpf = Column(String, unique=True, index=True)
    data_registro = Column(DateTime)

    encomendas = relationship("Encomenda", back_populates="cliente")


class Motorista(Base):
    __tablename__ = "motoristas"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idade = Column(Integer)
    nome = Column(String)
    telefone = Column(String)
    endereco = Column(String)
    email = Column(String, unique=True, index=True)
    status_ativo = Column(Boolean, default=True)
    cpf = Column(String, unique=True, index=True)

    veiculos = relationship("Veiculo", back_populates="motorista")
    encomendas = relationship("Encomenda", back_populates="motorista")


class Veiculo(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    motorista_id = Column(Integer, ForeignKey("motoristas.id"), nullable=True)
    marca = Column(String)
    modelo = Column(String)
    placa = Column(String, unique=True, index=True)
    ano = Column(Integer, nullable=False)
    status_ativo = Column(Boolean, default=True)

    motorista = relationship("Motorista", back_populates="veiculos")
    encomendas = relationship("Encomenda", back_populates="veiculo")


class Encomenda(Base):
    __tablename__ = 'encomendas'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    quantidade = Column(Integer)
    descricao = Column(String)
    prazo_entrega = Column(DateTime)
    data_pedido = Column(DateTime, default=datetime.utcnow)
    status_encomenda = Column(Boolean)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))

    cliente = relationship('Cliente', back_populates='encomendas')
    motorista = relationship('Motorista', back_populates='encomendas')
    veiculo = relationship('Veiculo', back_populates='encomendas')
    fornecedor = relationship('Fornecedor', back_populates='encomendas')
    pagamentos = relationship('Pagamento', back_populates='encomenda')
    produtos = relationship('Produto', secondary=encomenda_produto_association, back_populates='encomendas')


class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    email = Column(String, unique=True, index=True)
    status_ativo = Column(Boolean, default=True)
    cnpj = Column(String, unique=True, index=True)

    encomendas = relationship("Encomenda", back_populates="fornecedor")
    produtos = relationship("Produto", back_populates="fornecedor")


class Pagamento(Base):
    __tablename__ = "pagamentos"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    encomenda_id = Column(Integer, ForeignKey('encomendas.id'))
    valor = Column(Integer, nullable=False)
    data_pagamento = Column(DateTime, default=datetime.utcnow)
    metodo_pagamento = Column(String)

    encomenda = relationship('Encomenda', back_populates='pagamentos')


class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String)
    preco = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    data_criacao = Column(DateTime, default=datetime.utcnow)

    categoria = relationship('Categoria', back_populates='produtos')
    fornecedor = relationship('Fornecedor', back_populates='produtos')
    encomendas = relationship('Encomenda', secondary=encomenda_produto_association, back_populates='produtos')


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(String)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    produtos = relationship('Produto', back_populates='categoria')
