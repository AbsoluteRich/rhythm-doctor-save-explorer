from hashlib import md5

import json5
from rich.progress import Progress
from rich.table import Table

import core


# Might extend this to show other hidden bits about custom levels, but for now just showing the ranks is good enough
def walk_through_settings(save: dict) -> None:
    custom_levels = {}

    table = Table(title="Custom Levels")
    table.add_column("Level")
    table.add_column("Rank")

    for key in save:
        if key.startswith("CustomLevel_"):
            custom_levels[key[12:-7]] = save[key]

    for level in core.CUSTOM_LEVELS_FOLDER.iterdir():
        with Progress() as progress:
            progress_bar = progress.add_task(
                f"Processing {level.stem}...", start=False, total=None
            )
            # These two lines make type checkers shut up about unbound variables
            level_hash = ""
            song = ""

            with open(level / "main.rdlevel", encoding="utf-8-sig") as f:
                # JSON 5 allows trailing commas, which level files include
                try:
                    level_data = json5.load(f)

                    # A level's ID, which can be used to match them to data in settings.rdsave, is the author + artist + song name through MD5
                    # Source: https://discord.com/channels/296802696243970049/298297906509774848/1287309972018827397
                    author = level_data["settings"]["author"]
                    artist = level_data["settings"]["artist"]
                    song = level_data["settings"]["song"]

                    level_hash = md5(
                        author.encode() + artist.encode() + song.encode()
                    ).hexdigest()

                except ValueError:
                    # FIXME:
                    #   Some levels have malformed JSON which causes JSON 5 to freak out, but now I'm left with an unfinished level reading
                    #   The solution is to stream the JSON file so I can just read the settings section, but that's a headache in enough of itself, so this is a temporary fix
                    pass

            if level_hash:
                description = f"{song}: "
                try:
                    description += custom_levels[level_hash]
                except KeyError:
                    # Custom levels are aesthetically represented as syringes, and RD adds save file entries when you first attempt them and they are unsealed
                    description += "Sealed."
            else:
                description = f"Error while processing {level.stem}!"

            progress.update(progress_bar, description=description)

    core.console.rule()
    core.console.print(table)  # Todo: Move the extracted data into the table
