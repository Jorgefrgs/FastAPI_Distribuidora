from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:862100@localhost/db_fastapi_distribuidora"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    telefone = Column(String)
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
    email = Column(String)
    status_ativo = Column(Boolean, default=True)
    cpf = Column(String, unique=True, index=True)

    veiculos = relationship("Veiculo", back_populates="motorista")
    encomendas = relationship("Encomenda", back_populates="motorista")

class Veiculo(Base):
    __tablename__ = "veiculos"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    motorista_id = Column(Integer, ForeignKey("motoristas.id"))
    marca = Column(String)
    modelo = Column(String)
    ano = Column(Integer)
    status_ativo = Column(Boolean, default=True)

    motorista = relationship("Motorista", back_populates="veiculos")
    encomendas = relationship("Encomenda", back_populates="veiculo")

class Encomenda(Base):
    __tablename__ = 'encomendas'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
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
