from pathlib import Path


class FileStore:
    def __init__(self, project_root="./ladybug/"):
        self.project_root = Path(project_root).mkdir(
            exist_ok=True
        )  # Creates the project root if we didn't have it already.
