from apps.users.models import UserHealthData
from apps.common.base_repository import BaseRepository

class UserHealthDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserHealthData)