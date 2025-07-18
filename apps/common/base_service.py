class BaseService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        """Lấy tất cả các bản ghi."""
        return self.repository.get_all()

    def get_by_id(self, pk: int):
        """Lấy một bản ghi theo ID."""
        return self.repository.get_by_id(pk)
    
    def filter(self, **kwargs):
        """Lọc các bản ghi theo điều kiện."""
        return self.repository.filter(**kwargs)

    def create(self, **kwargs):
        """Tạo một bản ghi mới."""
        return self.repository.create(**kwargs)

    def update(self, pk: int, **kwargs):
        """Cập nhật một bản ghi theo ID."""
        instance = self.repository.get_by_id(pk)
        if not instance:
            raise ValueError("Instance not found")
        return self.repository.update(instance, **kwargs)

    def delete(self, pk: int):
        """Xóa một bản ghi theo ID."""
        instance = self.repository.get_by_id(pk)
        if not instance:
            raise ValueError("Instance not found")
        self.repository.delete(instance)