import requests
import configparser


class Config:
    AUTH_TOKEN = ""
    DOWNLOAD_FOLDER = ""
    DO_DOWNLOAD = False
    DO_DELETE = False
    EXCLUDE_RECORDING_IDS = []
    DO_WRITE_DOWNLOADED_LIST = False
    DO_WRITE_DELETED_LIST = False

    # API endpoints
    GET_ALL_RECORDINGS_ENDPOINT = "https://api.placetel.de/v2/recordings?page={}"
    GET_A_RECORDING_ENDPOINT = "https://api.placetel.de/v2/recordings/{}"
    DELETE_A_RECORDING_ENDPOINT = "https://api.placetel.de/v2/recordings/{}"

    def __init__(self):
        configfile = "settings.ini"

        config = configparser.RawConfigParser()
        config.read(configfile)

        if "AUTH_TOKEN" in config["DEFAULT"]:
            Config.AUTH_TOKEN = config["DEFAULT"]["AUTH_TOKEN"]

        if "DOWNLOAD_FOLDER" in config["DEFAULT"]:
            Config.DOWNLOAD_FOLDER = config["DEFAULT"]["DOWNLOAD_FOLDER"]

        if "DO_DOWNLOAD" in config["DEFAULT"]:
            if config["DEFAULT"]["DO_DOWNLOAD"].lower() in [
                "true",
                "t",
                "yes",
                "y",
            ]:
                Config.DO_DOWNLOAD = True

        if "DO_DELETE" in config["DEFAULT"]:
            if config["DEFAULT"]["DO_DELETE"].lower() in [
                "true",
                "t",
                "yes",
                "y",
            ]:
                Config.DO_DELETE = True

        if "EXCLUDE_RECORDING_IDS" in config["DEFAULT"]:
            for element in config["DEFAULT"]["EXCLUDE_RECORDING_IDS"].split(","):
                try:
                    Config.EXCLUDE_RECORDING_IDS.append(int(element))
                except ValueError:
                    pass

        if "DO_WRITE_DOWNLOADED_LIST" in config["DEFAULT"]:
            if config["DEFAULT"]["DO_WRITE_DOWNLOADED_LIST"].lower() in [
                "true",
                "t",
                "yes",
                "y",
            ]:
                Config.DO_WRITE_DOWNLOADED_LIST = True

        if "DO_WRITE_DELETED_LIST" in config["DEFAULT"]:
            if config["DEFAULT"]["DO_WRITE_DELETED_LIST"].lower() in [
                "true",
                "t",
                "yes",
                "y",
            ]:
                Config.DO_WRITE_DELETED_LIST = True

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


class Recordings(object):
    """Recordings is a Generator to retrieve pages of recordings from the API
    it returns one page from the API at a time
    one page is a list of at least one recording and up to 25 recordings

    this Generator implements caching and does not refresh the cache on a 2nd run
    if you get 20 pages on the first execution you will get the same 20 pages on the 2nd

    Returns:
        list: list of 1 to 25 recordings API objects
    """

    max_pages = 0
    recordings_pages = []

    def __init__(self) -> None:
        self.page = 1

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()


def download_all_recordings() -> None:
    pass


def delete_all_recordings() -> None:
    pass


if __name__ == "__main__":
    # read the config file
    Config()

    if Config.DO_DOWNLOAD:
        download_all_recordings()

    if Config.DO_DELETE:
        delete_all_recordings()
