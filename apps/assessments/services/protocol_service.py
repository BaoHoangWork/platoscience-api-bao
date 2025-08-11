from apps.common.base_service import BaseService
from apps.assessments.repositories.protocol_repository import ProtocolRepository

class ProtocolService(BaseService):
    def __init__(self):
        super().__init__(ProtocolRepository())