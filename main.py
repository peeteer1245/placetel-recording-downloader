import os
import pathlib
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
    GET_ALL_RECORDINGS_ENDPOINT = (
        "https://api.placetel.de/v2/recordings?page={}&order=asc"
    )
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

    is_fully_cached = False
    recordings_pages = []

    # log all requests for error dumping
    _record_of_all_requests = ["timestamp;API_endpoint;HTTP_status_code;misc"]
    _dump_format = "{};{};{};{}"

    def __init__(self) -> None:
        self.current_page = 0
        self.today = (
            datetime.now()
            .astimezone()
            .replace(hour=0, minute=0, second=0, microsecond=0)
        )

    def __iter__(self):
        return self

    def __next__(self):
        self.current_page += 1

        if Recordings.is_fully_cached:
            # we have already downloaded everything there is in a previous run

            # exit if we have reached the end of the cached recording pages
            if self.current_page > len(Recordings.recordings_pages):
                raise StopIteration()

            return Recordings.recordings_pages[self.current_page - 1]
        else:
            # we are downloading pages for the first time
            all_recordings_endpoint = Config.GET_ALL_RECORDINGS_ENDPOINT.format(
                self.current_page
            )
            recordings_page = Recordings._authorized_http_get(all_recordings_endpoint)

            # dump if a request goes wrong
            if recordings_page.status_code != 200:
                dump_str = Recordings._dump_format.format(
                    datetime.now().isoformat(),
                    recordings_page.url,
                    recordings_page.status_code,
                    "failed request",
                )
                Recordings._record_of_all_requests.append(dump_str)

                Recordings._dump()
                recordings_page.raise_for_status()

            # filter recordings to only allow recordings from before today
            filtered_recordings = []
            for recording in recordings_page.json():
                if datetime.fromisoformat(recording["time"]) < self.today:
                    filtered_recordings.append(recording)
                else:
                    # because the endpoint is sorted by date asc
                    # we can assume all further recordings are from today
                    break

            if len(filtered_recordings) > 0:
                Recordings.recordings_pages.append(filtered_recordings)
                return filtered_recordings
            else:
                Recordings.is_fully_cached = True
                raise StopIteration()

    @staticmethod
    def _dump():
        # TODO: maybe dump _record_of_all_requests to .csv?
        # TODO: maybe dump recordings_pages to .json?
        for row in Recordings._record_of_all_requests:
            print(row)

    @staticmethod
    def _authorized_http_get(url: str) -> requests.Response:
        """makes a authorized http get and returns response object

        Args:
            url (str): url to HTTP GET

        Returns:
            requests.Response: Response Object
        """

        headers = {"Authorization": Config.AUTH_TOKEN}

        r = requests.get(url, headers=headers)

        dump_str = Recordings._dump_format.format(
            datetime.now().isoformat(), r.url, r.status_code, "HTTP GET"
        )
        Recordings._record_of_all_requests.append(dump_str)

        return r

    @staticmethod
    def _authorized_http_delete(url: str) -> requests.Response:
        """makes a authorized http delete and returns response object

        Args:
            url (str): url to HTTP DELETE

        Returns:
            requests.Response: Response Object
        """

        headers = {"Authorization": Config.AUTH_TOKEN}

        r = requests.delete(url, headers=headers)

        dump_str = Recordings._dump_format.format(
            datetime.now().isoformat(), r.url, r.status_code, "HTTP DELETE"
        )
        Recordings._record_of_all_requests.append(dump_str)

        return r

    @staticmethod
    def delete_by_id(id: int) -> None:
        """delete a recording drom Placetel servers by id

        Args:
            id (int): id of the recording to be deleted
        """

        url = Config.DELETE_A_RECORDING_ENDPOINT.format(id)

        r = Recordings._authorized_http_delete(url)

        # dump if a request goes wrong
        if r.status_code != 200 or r.status_code != 204:
            dump_str = Recordings._dump_format.format(
                datetime.now().isoformat(),
                r.url,
                r.status_code,
                "failed request",
            )
            Recordings._record_of_all_requests.append(dump_str)

            Recordings._dump()
            r.raise_for_status()

        return


def save_to_file(content: bytes, filename: str) -> None:
    with open(filename, "wb") as f:
        f.write(content)
    return


def download_all_recordings() -> None:
    if not os.path.exists(Config.DOWNLOAD_FOLDER):
        print(
            "{} does not exist. Please create the directory.".format(
                Config.DOWNLOAD_FOLDER
            )
        )
        quit()

    current_recording = 0

    for recording_collection in Recordings():
        for recording in recording_collection:
            current_recording += 1

            print("{} | downloading".format(current_recording))

            r = Recordings._authorized_http_get(recording["file"])

            # dump if a request goes wrong
            if r.status_code != 200:
                dump_str = Recordings._dump_format.format(
                    datetime.now().isoformat(),
                    r.url,
                    r.status_code,
                    "failed request",
                )
                Recordings._record_of_all_requests.append(dump_str)

                Recordings._dump()
                r.raise_for_status()

            folder = pathlib.PurePath(Config.DOWNLOAD_FOLDER)

            filename = pathlib.PurePath(
                "{}_{}_{}_{}.mp3".format(
                    recording["time"],
                    recording["direction"],
                    recording["from"],
                    recording["to"],
                )
            )

            print("{} | saving".format(current_recording))

            save_to_file(r.content, str(folder / filename))


def delete_all_recordings() -> None:
    # Temporary FIX #6
    for recording_collection in Recordings():
        for recoding in recording_collection:
            pass

    current_recording = 0

    for recording_collection in Recordings():
        for recording in recording_collection:
            current_recording += 1

            print("{} | deleting".format(current_recording))

            Recordings.delete_by_id(recording["id"])


def main():
    # read the config file
    Config()

    if Config.DO_DOWNLOAD:
        download_all_recordings()

    if Config.DO_DOWNLOAD and Config.DO_DELETE:
        input("Please verify all files (press enter to continue)")

    if Config.DO_DELETE:
        delete_all_recordings()


if __name__ == "__main__":
    main()
