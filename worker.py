import json
import redis
from kafka import KafkaConsumer
from src.infrastructure.database import SessionLocal, RequestModel
from src.domain.models import RequestStatus

# TODO: As credenciais de conexão do Redis e do Kafka devem ser externalizadas via variáveis de ambiente (.env) em produção.
# Conecta com o Redis (nosso cache ultra rápido)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Conecta com o Kafka para ler o tópico
consumer = KafkaConsumer(
    'solicitacoes_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', # Lê as mensagens desde o começo (vai processar os testes anteriores)
    enable_auto_commit=True,
    group_id='bamaq-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def processar_solicitacoes():
    print("🎧 Worker iniciado! Aguardando mensagens no Kafka...")
    
    for message in consumer:
        dados = message.value
        request_id = dados['id']
        valor = dados['value']
        
        print(f"\n📦 Nova mensagem recebida do Kafka: ID {request_id} | Valor: R$ {valor}")
        
        # Regra de Negócio: Aprovar ou mandar para revisão manual
        if valor > 10000:
            novo_status = RequestStatus.MANUAL_REVIEW
        else:
            novo_status = RequestStatus.APPROVED
            
        print(f"🧠 Avaliação concluída. Novo status: {novo_status.value}")
        
        # Atualiza no MySQL
        db = SessionLocal()
        try:
            pedido_db = db.query(RequestModel).filter(RequestModel.id == request_id).first()
            if pedido_db:
                pedido_db.status = novo_status
                db.commit()
                print("✅ Status atualizado com sucesso no MySQL!")
                
                # Salva no Redis (para consultas rápidas)
                redis_client.set(f"status_pedido:{request_id}", novo_status.value)
                print("🚀 Status salvo no cache (Redis)!")
        finally:
            db.close()

if __name__ == "__main__":
    processar_solicitacoes()