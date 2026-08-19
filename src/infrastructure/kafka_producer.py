import json
from kafka import KafkaProducer

# TODO: Em produção, o bootstrap_server deve vir de uma variável de ambiente (ex: os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
# Configura a conexão com o Kafka que está rodando no Docker
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Função para enviar a mensagem
def publish_request_created(request_id: str, customer_id: str, value: float):
    # Montamos o "pacote" de dados que será enviado
    message = {
        "id": request_id,
        "customer_id": customer_id,
        "value": value,
        "status": "PENDING"
    }
    
    # Enviamos para um "tópico" (fila) chamado 'solicitacoes_topic'
    producer.send('solicitacoes_topic', message)
    producer.flush() # Garante que a mensagem saia do nosso app e vá para o Kafka
    print(f"Mensagem enviada para o Kafka: {message}")