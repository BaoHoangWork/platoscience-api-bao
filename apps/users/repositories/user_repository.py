from apps.users.models import User
from apps.common.base_repository import BaseRepository 

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_credentials(self, email: str, password: str):
        user = self.filter(email=email, password=password)
        
        return user.first()
    
    def get_by_email(self, email: str):
        return self.filter(email=email).first()
