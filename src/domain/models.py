import enum
import uuid
from dataclasses import dataclass

# Definimos os status possíveis da solicitação
class RequestStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    MANUAL_REVIEW = "MANUAL_REVIEW"

@dataclass
class RequestEntity:
    customer_id: str
    value: float
    id: str = None
    status: RequestStatus = RequestStatus.PENDING

    # Essa função roda automaticamente ao criar um RequestEntity
    def __post_init__(self):
        # Cria um identificador único se não for passado
        if self.id is None:
            self.id = str(uuid.uuid4())