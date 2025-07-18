from apps.assessments.models import SuggestedProtocol
from apps.common.base_repository import BaseRepository

class SuggestedProtocolRepository(BaseRepository):
    def __init__(self):
        super().__init__(SuggestedProtocol)