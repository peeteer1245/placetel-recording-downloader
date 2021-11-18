import requests
import configparser


class Config:
    AUTH_TOKEN = ""
    DOWNLOAD_FOLDER = ""
    DELETE_AFTER_DOWNLOAD = False

    # API endpoints
    GET_ALL_RECORDINGS_ENDPOINT = "https://api.placetel.de/v2/recordings"
    GET_A_RECORDING_ENDPOINT = "https://api.placetel.de/v2/recordings/{}"
    DELETE_A_RECORDING_ENDPOINT = "https://api.placetel.de/v2/recordings/{}"

    # Boilerplate examples
    # TODO: remove boilerplate code
    BOOLEAN = False
    STRING = ""
    INTEGER = 2

    def __init__(self):
        configfile = "settings.ini"

        config = configparser.RawConfigParser()
        config.read(configfile)

        if "AUTH_TOKEN" in config["DEFAULT"]:
            Config.AUTH_TOKEN = config["DEFAULT"]["AUTH_TOKEN"]

        if "DOWNLOAD_FOLDER" in config["DEFAULT"]:
            Config.DOWNLOAD_FOLDER = config["DEFAULT"]["DOWNLOAD_FOLDER"]

        if "DELETE_AFTER_DOWNLOAD" in config["DEFAULT"]:
            if config["DEFAULT"]["DELETE_AFTER_DOWNLOAD"].lower() in [
                "true",
                "t",
                "yes",
                "y",
            ]:
                Config.DELETE_AFTER_DOWNLOAD = True

        if "GET_ALL_RECORDINGS_ENDPOINT" in config["DEFAULT"]:
            Config.GET_ALL_RECORDINGS_ENDPOINT = config["DEFAULT"][
                "GET_ALL_RECORDINGS_ENDPOINT"
            ]

        if "GET_A_RECORDING_ENDPOINT" in config["DEFAULT"]:
            Config.GET_A_RECORDING_ENDPOINT = config["DEFAULT"][
                "GET_A_RECORDING_ENDPOINT"
            ]

        if "DELETE_A_RECORDING_ENDPOINT" in config["DEFAULT"]:
            Config.DELETE_A_RECORDING_ENDPOINT = config["DEFAULT"][
                "DELETE_A_RECORDING_ENDPOINT"
            ]

        # Boilerplate examples
        # TODO: remove boilerplate code
        if "BOOLEAN" in config["DEFAULT"]:
            if config["DEFAULT"]["BOOLEAN"].lower() in ["true", "t", "yes", "y"]:
                Config.BOOLEAN = True

        if "STRING" in config["DEFAULT"]:
            Config.STRING = config["DEFAULT"]["STRING"]

        if "INTEGER" in config["DEFAULT"]:
            Config.INTEGER = int(config["DEFAULT"]["INTEGER"])


def authorized_http_get(url: str) -> requests.Response:
    """makes a authorized http get and returns response object

    Args:
        url (str): url to HTTP GET

    Returns:
        requests.Response: Response Object
    """
    headers = {"Authorization": Config.AUTH_TOKEN}

    r = requests.get(url, headers=headers)

    return r


def authorized_http_delete(url: str) -> requests.Response:
    """makes a authorized http delete and returns response object

    Args:
        url (str): url to HTTP DELETE

    Returns:
        requests.Response: Response Object
    """
    headers = {"Authorization": Config.AUTH_TOKEN}

    r = requests.delete(url, headers=headers)

    return r


if __name__ == "__main__":
    # read the config file
    Config()
