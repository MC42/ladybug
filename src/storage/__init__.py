from pathlib import Path
import json


class FileStore:
    def __init__(self):
        self.project_root = Path("./datastore/")

        self.project_root.mkdir(
            exist_ok=True
        )  # Creates the project root if we didn't have it already.

        self.config_file = self.loadConfigFile()

    def loadConfigFile(self) -> list:
        self.config_file_path = self.project_root.joinpath("config.json")

        if not self.config_file_path.exists():

            # We're making the config options in-line.  There must be a better way to handle this type of abstract k/v store, but for now this will work.
            # Down the line, take a look at shelve maybe?
            config = {}
            config["pixels_per_mm"] = None
            config["serial_port"] = "COM4"
            config["baud_rate"] = 115_200

            with open(self.config_file_path, "w") as file_to_out:
                file_to_out.write(json.dumps(config, indent=4))

        config = json.loads(open(self.config_file_path.absolute(), "r").read())

        return config
