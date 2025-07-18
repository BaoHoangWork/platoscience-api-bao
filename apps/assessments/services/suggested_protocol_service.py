from apps.assessments.repositories.protocol_repository import ProtocolRepository
from apps.assessments.repositories.suggested_protocol_repository import SuggestedProtocolRepository
from apps.common.base_service import BaseService


class SuggestedProtocolService(BaseService):
    def __init__(self):
        self.protocol_repo = ProtocolRepository()
        self.suggested_repo = SuggestedProtocolRepository()

    def create_suggested_protocols(self, assessment, first_protocol, second_protocol, third_protocol):
        protocols = self.protocol_repo.filter(id__in=[first_protocol, second_protocol, third_protocol])
        protocol_map = {p.id: p for p in protocols}
        return self.suggested_repo.create(
            assessment=assessment,
            first_protocol=protocol_map.get(first_protocol),
            second_protocol=protocol_map.get(second_protocol),
            third_protocol=protocol_map.get(third_protocol),
        )
