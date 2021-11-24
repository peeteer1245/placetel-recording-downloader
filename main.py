import requests
import configparser
from datetime import datetime


class Config:
    AUTH_TOKEN = ""
    DOWNLOAD_FOLDER = ""
    DO_DOWNLOAD = False
    DO_DELETE = False
    EXCLUDE_RECORDING_IDS = []
    DO_WRITE_DOWNLOADED_LIST = False
    DO_WRITE_DELETED_LIST = False

    # API endpoints
    GET_ALL_RECORDINGS_ENDPOINT = "https://api.placetel.de/v2/recordings?page={}&order=asc"
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


class Recordings(object):
    """Recordings is a Generator to retrieve pages of recordings from the API
    it will never return a recording of the current day
    it returns one page from the API at a time
    one page is a list of at least one recording and up to 25 recordings

    this Generator implements caching and does not refresh the cache on consecutive runs
    if you get 20 pages on the first execution you will get the same 20 pages on the 2nd

    Returns:
        list: list of 1 to 25 recordings API objects

    TODO: set the start and end filter in the API Request
    TODO: -> set the order to asc and stop when you get the first recording from today
    TODO: -> datetime.fromisoformat(date_string)
    TODO: -> today = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    """

    max_pages = 0
    recordings_pages = []

    # log all requests for error dumping
    _record_of_all_requests = ["timestamp;API_endpoint;HTTP_status_code;misc"]
    _dump_format = "{};{};{};{}"

    def __init__(self) -> None:
        self.current_page = 1

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration()

    def _dump(self):
        pass

    def _authorized_http_get(self, url: str) -> requests.Response:
        """makes a authorized http get and returns response object

        Args:
            url (str): url to HTTP GET

        Returns:
            requests.Response: Response Object
        """
        headers = {"Authorization": Config.AUTH_TOKEN}

        r = requests.get(url, headers=headers)

        return r

    def _authorized_http_delete(self, url: str) -> requests.Response:
        """makes a authorized http delete and returns response object

        Args:
            url (str): url to HTTP DELETE

        Returns:
            requests.Response: Response Object
        """
        headers = {"Authorization": Config.AUTH_TOKEN}

        r = requests.delete(url, headers=headers)

        return r


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
