import uuid
from http import HTTPStatus

import requests
from requests import Response

from dialogue import Dialogue, DialogueType
from entity import Entity


class EnchantusAPIClient:
    def __init__(self, api_token: str, base_url: str = 'http://EnchantusAPILB-1831778516.us-east-1.elb.amazonaws.com'):
        self.base_url = base_url
        self.api_token = api_token
        self.headers = {'token': self.api_token}

    def get_project_id(self):
        endpoint = f'{self.base_url}/project/id'
        response = requests.get(endpoint, headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            return None, response

        return response.json()['id'], response

    def add_dialogue(self,
                     dialogue_type: DialogueType,
                     content: str,
                     actor_id: uuid.UUID,
                     parent_id: uuid.UUID = None) -> (Dialogue, Response):
        endpoint = f'{self.base_url}/dialogue/add'
        data = {
            'type': dialogue_type,
            'content': content,
            'actor_id': actor_id
        }

        if parent_id:
            data['parent_id'] = parent_id

        response = requests.post(endpoint, json=data, headers=self.headers)
        if response.status_code != HTTPStatus.CREATED:
            return None, response

        return Dialogue.from_dict(response.json()), response

    def generate_dialogue(self, actor_id, parent_id) -> (Dialogue, Response):
        endpoint = f'{self.base_url}/dialogue/generate'
        data = {
            'parent_id': parent_id,
            'actor_id': actor_id
        }

        response = requests.post(endpoint, json=data, headers=self.headers)
        if response.status_code != HTTPStatus.CREATED:
            return None, response

        return Dialogue.from_dict(response.json()), response

    def create_entity(self, name, details) -> (Entity, Response):
        endpoint = f'{self.base_url}/entity/create'
        data = {
            'name': name,
            'details': details
        }

        response = requests.post(endpoint, json=data, headers=self.headers)
        if response.status_code != HTTPStatus.CREATED:
            return None, response

        return Entity.from_dict(data=response.json()), response

    def update_entity(self, entity_id, name, details) -> (Entity, Response):
        endpoint = f'{self.base_url}/entity/update'
        data = {
            'id': entity_id,
            'name': name,
            'details': details
        }

        response = requests.put(endpoint, json=data, headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            return None, response

        return Entity.from_dict(response.json()), response
