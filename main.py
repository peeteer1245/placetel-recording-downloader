import configparser


class Config:
    AUTH_TOKEN = ""
    DOWNLOAD_FOLDER = ""
    DELETE_AFTER_DOWNLOAD = False

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

        # Boilerplate examples
        # TODO: remove boilerplate code
        if "BOOLEAN" in config["DEFAULT"]:
            if config["DEFAULT"]["BOOLEAN"].lower() in ["true", "t", "yes", "y"]:
                Config.BOOLEAN = True

        if "STRING" in config["DEFAULT"]:
            Config.STRING = config["DEFAULT"]["STRING"]

        if "INTEGER" in config["DEFAULT"]:
            Config.INTEGER = int(config["DEFAULT"]["INTEGER"])


def authorized_get(url):
    headers = {
        "Authorization": Config.AUTH_TOKEN
    }

    # url = "https://api.placetel.de/v2/recordings"
    # url = "https://api.placetel.de/v2/recordings/42069"
    # url = "https://storage.googleapis.com/placetel-documents/uploads/recording/file/42069/..."

    r = requests.get(url, headers=headers)

    return r


if __name__ == "__main__":
    pass
