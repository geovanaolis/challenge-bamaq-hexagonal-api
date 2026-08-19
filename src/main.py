from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import redis
from src.domain.models import RequestEntity
from src.infrastructure.database import SessionLocal, RequestModel
from src.infrastructure.kafka_producer import publish_request_created

app = FastAPI(title="Desafio BAMAQ Capital - API")
# Conectando a API ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Definimos o "Schema" (como a API espera receber o JSON)
class RequestInput(BaseModel):
    customer_id: str
    value: float = Field(gt=0, description="O valor da solicitação deve ser maior que zero") # Adicionado Field para validar o valor númerico

# Função auxiliar para abrir e fechar a conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criamos o endpoint POST /requests
@app.post("/requests", status_code=201)
def create_request(data: RequestInput, db: Session = Depends(get_db)):
    # Usamos o nosso Domínio para criar a solicitação
    entity = RequestEntity(customer_id=data.customer_id, value=data.value)
    
    # Convertemos para o formato do SQLAlchemy e salvamos no MySQL
    db_request = RequestModel(
        id=entity.id,
        customer_id=entity.customer_id,
        value=entity.value,
        status=entity.status
    )
    db.add(db_request)
    db.commit() # Confirma a transação no banco de dados

    # Publica a mensagem no Kafka
    publish_request_created(
        request_id=entity.id, 
        customer_id=entity.customer_id, 
        value=entity.value
    )
    
    # Retornar o ID gerado conforme o fluxo da arquitetura
    return {"id": entity.id, "message": "Solicitação criada com status PENDING"}

# Criamos o endpoint GET /requests/{id}
@app.get("/requests/{request_id}")
def get_request_status(request_id: str, db: Session = Depends(get_db)):
    # Tenta buscar no Redis primeiro (muito mais rápido)
    status_cache = redis_client.get(f"status_pedido:{request_id}")
    if status_cache:
        return {"id": request_id, "status": status_cache, "source": "redis (cache)"}
    
    # Se não achar no cache, busca no banco de dados MySQL
    pedido_db = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not pedido_db:
        return {"error": "Solicitação não encontrada"}
        
    return {"id": request_id, "status": pedido_db.status, "source": "mysql (db)"}