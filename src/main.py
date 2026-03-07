import json
import os
import pathlib

import json5
import pick
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Stringifying the environment variable makes type checkers shut up
save_folder = (
    pathlib.Path(str(os.getenv("LOCALAPPDATA")) + "Low")
    / "7th Beat Games"
    / "Rhythm Doctor"
)
saves = {}

with open("data.json5") as f:
    level_mappings = json5.load(f)

console = Console()


# Todo
def walk_through_settings(rd_save: dict):
    # https://discord.com/channels/296802696243970049/298297906509774848/1287309972018827397
    # it's author + artist + song through md5
    table = Table("Custom Levels")
    print(table)


def walk_through_save(rd_save: dict):
    for act in level_mappings:
        table = Table(title=act)
        table.add_column("Level")
        table.add_column("Rank")
        table.add_column("Attempts")  # Not implemented yet

        for level_id in level_mappings[act]:
            try:
                rank = rd_save[f"Level_{level_id}_rank"]
            except KeyError:
                table.add_row("???", "Unplayed", "0")
                continue

            designator = Text(
                level_mappings[act][level_id]["designator"], style="bright_green"
            )  # Close enough to lime
            name = Text(level_mappings[act][level_id]["name"], style="bright_cyan")

            try:
                attempts = rd_save[f"{level_id}_tries"]
            except KeyError:
                attempts = 0
            attempts = str(attempts)

            if level_mappings[act][level_id].get("is_boss"):
                # Completed w/o checkpoints is a completely separate thing?? How many boss ranks are there
                name = name + Text(" (Boss)", style="magenta")

                if rank == "NotFinished":
                    rank = "Incomplete"
                elif rank == "A":
                    # RD doesn't give a rank to bosses, it just marks it as A if you've completed it
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
                    attempts = (
                        f"{attempts} (Score: {rd_save[f'Level_{level_id}_score']})"
                    )
                except KeyError:
                    # Prevent crashes if a player hasn't attempted the bonus level yet
                    pass

            table.add_row(designator + " " + name, rank, attempts)

        print(table)


if __name__ == "__main__":
    for save_file in save_folder.glob("*.rdsave"):
        # RD saves actually start with a UTF-8 BOM, so the old solution of slicing off the first few characters was incorrect
        with save_file.open(encoding="utf-8-sig") as f:
            save = json.loads(f.read())
            saves[save_file.name.split(".")[0]] = save

    option, _ = pick.pick(
        list(saves.keys()),
        "Select which save file you wish to browse:",
    )

    if option == "settings":
        walk_through_settings(saves["settings"])
    else:
        walk_through_save(saves[option])
