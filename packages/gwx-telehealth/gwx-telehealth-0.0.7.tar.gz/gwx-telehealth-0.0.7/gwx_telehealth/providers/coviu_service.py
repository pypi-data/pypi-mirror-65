import json
import requests

from gwx_telehealth.abstract_telehealth_service import AbstractTelehealthService
from gwx_telehealth.services.auth_service import AuthService


class CoviuService(AbstractTelehealthService):
    access_token: dict = None

    endpoint: str = None

    def __init__(self, config: dict):
        auth_service = AuthService(
            f'{config.get("endpoint")}/auth/token',
            config.get('api_key'),
            config.get('api_key_secret'),
            config.get('grant_type')
        )
        super().__init__(config, auth_service)
        self.endpoint = config.get('endpoint')
        self.access_token = self.auth_service.create_access_token()

    def create_room(self, data: dict) -> dict:
        body = json.dumps(data)

        result = requests.post(
            f'{self.endpoint}/sessions',
            data=body,
            headers=self.__auth_header(self.access_token['access_token'])
        )

        return result.json()

    def get_room(self, room_id: str) -> dict or None:
        result = requests.get(
            f'{self.endpoint}/sessions/{room_id}',
            headers=self.__auth_header(self.access_token['access_token'])
        )

        return result.json()

    def list_rooms(self) -> dict or None:
        result = requests.get(
            f'{self.endpoint}/sessions',
            headers=self.__auth_header(self.access_token['access_token'])
        )

        return result.json()

    @staticmethod
    def __auth_header(access_token: str) -> dict:
        return {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
