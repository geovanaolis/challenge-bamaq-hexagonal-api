from sqlalchemy import create_engine, Column, String, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from src.domain.models import RequestStatus

# TODO: Em um ambiente de produção, estas credenciais devem vir de variáveis de ambiente (.env) ou Vault.
# URL de conexão com o MySQL que está rodando no Docker
# Formato: mysql+driver://usuario:senha@host:porta/nome_do_banco
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/bamaq_db"

# Configuração do motor do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definição de como a tabela 'requests' será criada no MySQL
class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)

# Comando para criar a tabela no banco de dados caso ela não exista
Base.metadata.create_all(bind=engine)