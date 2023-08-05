from importlib import util

from gwx_telehealth import config
from gwx_telehealth.abstract_telehealth_service import AbstractTelehealthService


class ServiceLocatorService:
    """Service locator class, responsible for loading the
    current service specified within the provider config_parser.

    :param provider_name str value of the provider service name
    """

    # The class name of a specific provider service.
    provider_service_name: str = None

    # The provider service file path.
    provider_service_file: str = None

    # The providers file name ie: `coviu`
    provider_service_file_name: str = None

    def __init__(self, provider_name: str):
        self.__set_provider_service_name(provider_name)
        self.__set_provider_service_file_name(provider_name)
        self.__set_provider_service_file(self._get_provider_service_file_name())

    def __set_provider_service_name(self, provider_name: str) -> None:
        """Identify the class name of the provider service class.

        :return: None
        """
        self.provider_service_name = f'{str.title(provider_name)}Service'

    def __set_provider_service_file_name(self, provider_name: str) -> None:
        """Identify the file_name of the provider service class.

        :param provider_name: the base name of a provider service ie:
            `coviu`, `spruce`
        :return: None
        """

        self.provider_service_file_name = f'{str.lower(provider_name)}_service'

    def _get_provider_service_file_name(self) -> str:
        """Return the string value of the resolved `provider_service_file`

        :return: string value for the `provider_service_file`
        """
        return self.provider_service_file_name

    def _get_provider_service_name(self) -> str:
        """The supplied name of the provider service class.

        :return: return the string value of the class.
        """
        return self.provider_service_name

    def __set_provider_service_file(self, provider_service_name: str) -> None:
        """Identify the python file of the provider service class,
        then populate it to a variable.

        :return: None.
        """
        provider_service_file = f'{config["provider_path"]}/{provider_service_name}.py'

        try:
            open(provider_service_file)
        except FileExistsError:
            raise FileExistsError(
                [config['package_name'], f'Provider Service file: {provider_service_file} not found.']
            )

        self.provider_service_file = provider_service_file

    def __get_provider_service_file(self) -> str:
        """The identified python file of the provider service class.

        :return: return the string value of the python file.
        """
        return f'{self.provider_service_file}'

    def get_provider(self) -> AbstractTelehealthService or None:
        """Provider service class specified in the config_parser file,
        this will throw an IO Error once the file supplied is non existing.

        :return: the resolved concrete instance found that is conforming
        to the AbstractTelehealthService class, or None if nothing is found.
        """
        provider_file = f'{self.__get_provider_service_file()}'
        service_name = f'{self._get_provider_service_name()}'

        try:

            file = open(provider_file)
        except IOError:
            print(f'File {provider_file} not found.')
            return None

        file.close()

        spec = util.spec_from_file_location(service_name, provider_file)

        service = util.module_from_spec(spec)
        spec.loader.exec_module(service)

        return getattr(service, service_name)
