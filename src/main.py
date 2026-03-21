import json
from hashlib import md5
from os import getenv
from pathlib import Path

import json5
import platformdirs
from pick import pick
from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.text import Text

# Stringifying the environment variable makes type checkers shut up about potentially None values
# (Every Windows setup should define Local AppData, and if it doesn't, something is very wrong)
save_folder = (
    Path(str(getenv("LOCALAPPDATA")) + "Low") / "7th Beat Games" / "Rhythm Doctor"
)
# Why is it just platformdirs that can accurately find the Documents folder??
custom_levels_folder = platformdirs.user_documents_path() / "Rhythm Doctor" / "Levels"
rd_saves = {}
custom_levels = {}

spoilers = False
spoiler_label = "Spoilers: OFF"

with open("data.json5") as f:
    level_mappings = json5.load(f)

console = Console()


# Might extend this to show other hidden bits about custom levels, but for now just showing the ranks is good enough
def walk_through_settings(save: dict):
    table = Table(title="Custom Levels")
    table.add_column("Level")
    table.add_column("Rank")

    for key in save:
        if key.startswith("CustomLevel_"):
            custom_levels[key[12:-7]] = save[key]

    for level in custom_levels_folder.iterdir():
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

    console.rule()
    print(table)  # Todo: Move the extracted data into the table


def walk_through_save(save: dict):
    for act in level_mappings:
        table = Table(title=act)
        table.add_column("Level")
        table.add_column("Rank")
        table.add_column("Attempts")

        for level_id in level_mappings[act]:
            try:
                rank = save[f"Level_{level_id}_rank"]
            except KeyError:
                table.add_row("???", "Unplayed", "0")
                continue

            designator = Text(
                level_mappings[act][level_id]["designator"], style="bright_green"
            )  # Close enough to lime
            name = Text(level_mappings[act][level_id]["name"], style="bright_cyan")

            try:
                attempts = save[f"{level_id}_tries"]
            except KeyError:
                attempts = 0
            attempts = str(attempts)

            if level_mappings[act][level_id].get("is_boss"):

                name = name + Text(" (Boss)", style="magenta")

                # RD doesn't give a rank to bosses, it just marks it as A if you've completed it
                if rank == "NotFinished":
                    rank = "Incomplete"
                elif rank == "A+":
                    # Completed w/o checkpoints is a completely separate thing?? How many boss ranks are there
                    rank = "Completed without checkpoints!"
                elif rank == "A":
                    rank = "Completed"
                elif rank == "S+":
                    rank = Text("Perfect!", style="yellow")
                else:
                    rank = "Unknown rank! Contact the repo owner!"
            else:
                if rank == "NotFinished":
                    rank = "Unplayed"
                elif (
                    rank.startswith("C") or rank.startswith("D") or rank.startswith("F")
                ):
                    rank = Text(rank, style="bright_black")
                elif rank.startswith("S"):
                    rank = Text(rank, style="yellow")

            if level_mappings[act][level_id].get("is_intermission"):
                name = name + Text(" (Intermission)", style="magenta")

            if level_mappings[act][level_id].get("is_bonus"):
                name = name + Text(" (Bonus)", style="magenta")
                try:
                    attempts = f"{attempts} (Score: {save[f'Level_{level_id}_score']})"
                except KeyError:
                    # Prevent crashes if a player hasn't attempted the bonus level yet
                    pass

            table.add_row(designator + " " + name, rank, attempts)

        print(table)


if __name__ == "__main__":
    # 100% save file, for reference: https://steamcommunity.com/app/774181/discussions/0/693120275093500198/

    for save_file in save_folder.glob("*.rdsave"):
        # RD saves actually start with a UTF-8 BOM, so the old solution of slicing off the first few characters was incorrect
        with save_file.open(encoding="utf-8-sig") as f:
            save = json.load(f)
            rd_saves[save_file.name.split(".")[0]] = save

    option, _ = pick(
        [spoiler_label] + list(rd_saves.keys()) + ["Exit"],
        "Select which save file you wish to browse:",
    )

    while True:
        if option == "Exit":
            break
        elif option == spoiler_label:
            spoilers = not spoilers
            spoiler_label = "Spoilers: ON" if spoilers else "Spoilers: OFF"
        elif option == "settings":
            walk_through_settings(rd_saves["settings"])
        else:
            walk_through_save(rd_saves[option])
