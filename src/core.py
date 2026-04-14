import json
from os import getenv
from pathlib import Path

import json5
import platformdirs
from rich.console import Console

# Stringifying the environment variable makes type checkers shut up about potentially None values
# (Every Windows setup should define Local AppData, and if it doesn't, something is very wrong)
SAVE_FOLDER = (
    Path(str(getenv("LOCALAPPDATA")) + "Low") / "7th Beat Games" / "Rhythm Doctor"
)
# Why is it just platformdirs that can accurately find the Documents folder??
CUSTOM_LEVELS_FOLDER = platformdirs.user_documents_path() / "Rhythm Doctor" / "Levels"

console = Console(record=True)


def load_mappings() -> dict:
    with open("data.json5") as f:
        return json5.load(f)


def load_save_files() -> dict:
    rd_saves = {}

    for save_file in SAVE_FOLDER.glob("*.rdsave"):
        # RD saves actually start with a UTF-8 BOM, so the old solution of slicing off the first few characters was incorrect
        with save_file.open(encoding="utf-8-sig") as f:
            save = json.load(f)
            rd_saves[save_file.name.split(".")[0]] = save

    return rd_saves
