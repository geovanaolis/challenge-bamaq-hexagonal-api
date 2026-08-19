from src.domain.models import RequestEntity, RequestStatus

def test_deve_criar_solicitacao_com_status_pending():
    # Prepara os dados
    customer_id = "12345"
    value = 5000.0
    
    # Executa a ação
    entity = RequestEntity(customer_id=customer_id, value=value)
    
    # Verifica (Assert) se o resultado é o esperado
    assert entity.customer_id == "12345"
    assert entity.value == 5000.0
    assert entity.status == RequestStatus.PENDING

def test_deve_gerar_uuid_automaticamente():
    # Executa a ação
    entity = RequestEntity(customer_id="999", value=100.0)
    
    # Verifica se o ID não é vazio e é uma string
    assert entity.id is not None
    assert isinstance(entity.id, str)
    assert len(entity.id) > 10 # UUIDs são textos longos