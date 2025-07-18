from apps.assessments.models.protocol_model import Protocol
from apps.common.base_repository import BaseRepository

class ProtocolRepository(BaseRepository):
    def __init__(self):
        super().__init__(Protocol)