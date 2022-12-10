import os
from pathlib import Path


def prepare_download_folders(download_path: str, folder_name: str, type: str) -> str:

    RES_PATH = os.path.join(
        download_path,
        "resources",
        folder_name,
    )
    Path(RES_PATH).mkdir(parents=True, exist_ok=True)
    if type == "Web":
        Path(RES_PATH, "fonts").mkdir(exist_ok=True)
        Path(RES_PATH, "images").mkdir(exist_ok=True)
    return RES_PATH
