import logging
import requests
import requests.packages
from typing import List, Dict
from json import JSONDecodeError
from .exceptions import PrintfulApiException
from .models.generic import Result


class RestAdapter:
    """
    Low level REST Adapter to provide a connection to the Printful API
    Based on https://www.pretzellogix.net/2021/12/08/step-2-write-a-low-level-rest-adapter/

    :param hostname: defaults to "api.printful.com"
    :type hostname: str, optional
    :param api_key: API Key used for authentication
    :type api_key: str
    :param ver: API version string, defaults to "v2"
    :type ver: str, optional
    :param ssl_verify: if having SSL/TLS cert validation issues turn off with `False`, defaults to `True`
    :type ssl_verify: bool, optional
    :param logger: defaults to None
    :type logger: logging.Logger, optional
    """

    def __init__(
        self,
        hostname: str = "api.printful.com",
        api_key: str = "",
        ver: str = "v2",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """
        Constructor method
        """
        self.url = f"https://{hostname}/{ver}"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()
        self._logger = logger or logging.getLogger(__name__)

    def _do(
        self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        """
        Private method for get(), post(), delete(), etc. methods

        :param http_method: GET, POST, DELETE, etc.
        :type http_method: str
        :param endpoint: URL Endpoint as a string
        :type endpoint: str
        :param ep_params: Dictionary of Endpoint parameters
        :type ep_params: Dict, optional
        :param data: Dictionary of data to pass to Printful API (Optional)
        :type data: Dict, optional
        :return: a printful Result object
        :rtype: printful.Result
        :raises: PrintfulApiException
        """
        full_url = self.url + endpoint
        headers = {"Authorization": f"Bearer {self._api_key}"}

        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise PrintfulApiException("Request failed") from e

        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise PrintfulApiException("Bad JSON in response") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200  # 200 to 299 is OK
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason
        )
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise PrintfulApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """
        Public GET method

        :param endpoint: URL Endpoint as a string
        :type endpoint: str
        :param ep_params: Dictionary of Endpoint parameters
        :type ep_params: Dict, optional
        :param data: Dictionary of data to pass to Printful API (Optional)
        :type data: Dict, optional
        :return: a printful Result object
        :rtype: printful.Result
        :raises: PrintfulApiException
        """
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Public POST method

        :param endpoint: URL Endpoint as a string
        :type endpoint: str
        :param ep_params: Dictionary of Endpoint parameters
        :type ep_params: Dict, optional
        :param data: Dictionary of data to pass to Printful API (Optional)
        :type data: Dict, optional
        :return: a printful Result object
        :rtype: printful.Result
        :raises: PrintfulApiException
        """
        return self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def delete(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        """
        Public POST method

        :param endpoint: URL Endpoint as a string
        :type endpoint: str
        :param ep_params: Dictionary of Endpoint parameters
        :type ep_params: Dict, optional
        :param data: Dictionary of data to pass to Printful API (Optional)
        :type data: Dict, optional
        :return: a printful Result object
        :rtype: printful.Result
        :raises: PrintfulApiException
        """
        return self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )
