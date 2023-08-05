import json
import base64
import requests

from gwx_telehealth import config


class AuthService:
    api_key: str = None

    api_key_secret: str = None

    token_endpoint: str = None

    grant_type: str = None

    def __init__(self, token_endpoint: str, api_key: str, api_key_secret: str, grant_type: str):
        """The auth service instance,
        this will manage all the authentication transactions needed by the consuming service.

        :param token_endpoint: str the token endpoint
        where the auth service will request for an access token
        :param api_key: str the api key of the consuming service
        :param api_key_secret: str the api key secret of the consuming service
        :param grant_type: str grant type required to specify grant to the access token
        """
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.grant_type = grant_type
        self.token_endpoint = token_endpoint

    def create_access_token(self) -> dict:
        """Initiate the authentication process
        and return the access token in json object file format.

        :return: dict
        """

        if config.get('cache_token') == 'Yes':
            if self.__get_existing_token() is not None:
                return self.__get_existing_token()

        token = requests.post(
            self.token_endpoint,
            data={'grant_type': self.grant_type},
            headers=self.__build_header()
        ).json()

        if config.get('cache_token') == 'Yes':
            self.__store_token_as_json(token)

        return token

    def refresh_access_token(self) -> dict:
        """Refresh the access token, then overwrite the existing token file.

        :return: dict the new access token after refresh.
        """
        if config.get('cache_token') == 'Yes':
            existing_token: dict = self.__get_existing_token()

            # noinspection PyBroadException
            try:
                token = requests.post(
                    self.token_endpoint,
                    data={'grant_type': 'refresh_token', 'refresh_token': existing_token.get('refresh_token', None)},
                    headers=self.__build_header()
                ).json()

                self.__store_token_as_json(token)

                return token
            except RuntimeError:
                print(RuntimeError(existing_token))

        return {}

    def __build_header(self) -> dict:
        """Build the header ready for the auth request.

        :return: dict
        """

        # @todo: for the time being this hardcoded due to time constraint,
        # @todo: but we'll move this to a factory that will have this decoupled
        to_encode = f'{self.api_key}:{self.api_key_secret}'
        return {
            'Authorization': f'Basic {base64.b64encode(to_encode.encode()).decode()}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def __store_token_as_json(token: dict):
        """Create the token json file that will be used on api transactions.

        :param token:
        :return:
        """
        token_file = None

        try:
            with open(f'{config.get("token_path")}/token.json', 'w') as token_file:
                json.dump(token, token_file)
        except IOError:
            raise IOError(f'Cannot write {token_file} to file')

    @staticmethod
    def __get_existing_token() -> dict or None:
        """Get an existing token recently generated,
        this will keep the service from invoking token requests,
        when there is still a valid token existing.

        :return: dict or None
        """

        # hard code the token.json file spec for now
        token_file = f'{config.get("token_path")}/token.json'
        try:

            file = open(token_file)
        except IOError:
            print(f'File {token_file} not found.')
            return None

        token = json.load(file)
        file.close()

        return token
