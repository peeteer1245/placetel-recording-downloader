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
    GET_ALL_RECORDINGS_ENDPOINT = "https://api.placetel.de/v2/recordings"
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


def get_all_recording_info() -> list:
    return []


def download_all_recordings(recordings: list) -> None:
    pass


def delete_all_recordings(recordings: list) -> None:
    pass


if __name__ == "__main__":
    # read the config file
    Config()

    list_of_recordings = get_all_recording_info()

    # filter the list of recordings
    # this way unwanted recordings never get downloaded or deleted
    filtered_list = []
    for element in list_of_recordings:
        if element["id"] not in Config.EXCLUDE_RECORDING_IDS:
            filtered_list.append(element)
    list_of_recordings = filtered_list
    del filtered_list

    if Config.DO_DOWNLOAD:
        download_all_recordings(list_of_recordings)

    if Config.DO_DELETE:
        delete_all_recordings(list_of_recordings)
