from environs import env
from .exceptions import PrintfulApiException

def get_api_token():
    """
    Loads the Printful API v2 access token from the environment or a .env file using the python environs package.

    :return: The access token as a string if found, raises an error if not found.
    """
    # Load environment variables from .env file
    env.read_env()

    # Get the access token from the environment
    access_token = env("PRINTFUL_AUTH_TOKEN")

    # Error handling if access token is not found
    if access_token is None:
        raise PrintfulApiException("PRINTFUL_AUTH_TOKEN not found in environment variables.")

    return access_token
