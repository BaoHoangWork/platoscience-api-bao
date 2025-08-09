from apps.common.base_service import BaseService
from apps.users.repositories.user_health_data_repository import UserHealthDataRepository

class UserHealthDataService(BaseService):
    def __init__(self):
        super().__init__(UserHealthDataRepository())