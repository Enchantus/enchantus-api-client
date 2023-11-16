import uuid


class Entity:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    details: dict

    def __init__(self,
                 entity_id: uuid.UUID,
                 project_id: uuid.UUID,
                 name: str,
                 details: dict):
        self.id = entity_id
        self.project_id = project_id
        self.name = name
        self.details = details

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'details': self.details,
        }

    @staticmethod
    def from_dict(data):
        return Entity(entity_id=data['id'],
                      project_id=data['project_id'],
                      name=data['name'],
                      details=data['details'])
