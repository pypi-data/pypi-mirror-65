from abc import abstractmethod

from gwx_telehealth.services.auth_service import AuthService


class AbstractTelehealthService:
    # The service that will be defined in each of the concrete provider class
    auth_service: AuthService = None

    # The defined configuration file
    config: dict = None

    def __init__(self, config: dict, auth_service: AuthService):
        self.config = config
        self.auth_service = auth_service

    @abstractmethod
    def create_room(self, data: dict) -> dict:
        """Checkout method, this will initiate a room.

        :param data: the parameters for the room creation.
        :return: structured value required for response composition.
        """
        pass

    @abstractmethod
    def get_room(self, room_id: str) -> dict or None:
        """Retrieve a specific room

        :param room_id: the primary id used to reference against an endpoint.
        :return: the retrieved record, null if none found.
        """
        pass

    @abstractmethod
    def list_rooms(self) -> dict or None:
        """Retrieve the list of rooms available for this user.

        :return: the list of rooms
        """
        pass
