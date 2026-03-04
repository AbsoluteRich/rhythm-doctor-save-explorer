import json
import os
import pathlib

import pick
from rich.console import Console
from rich.table import Table
from rich.text import Text

from data import level_mappings

save_folder = (
    # Stringifying the environment variable makes type checkers shut up
    pathlib.Path(str(os.getenv("LOCALAPPDATA")) + "Low")
    / "7th Beat Games"
    / "Rhythm Doctor"
)
saves = {}

console = Console()
print = console.print


def walk_through_settings(rd_save: dict):
    pass


def walk_through_save(rd_save: dict):
    # console.rule("Act 1")

    for act in level_mappings:
        table = Table(title=act)
        table.add_column("Level")
        table.add_column("Rank")
        table.add_column("Attempts")  # Not implemented yet

        for level_id in level_mappings[act]:
            designator = Text(
                    level_mappings[act][level_id]["designator"], style="bright_green"
                )  # Close enough to lime
            name = Text(level_mappings[act][level_id]["name"], style="bright_cyan")

            rank = rd_save[f"Level_{level_id}_rank"]

            try:
                attempts = rd_save[f"{level_id}_tries"]
            except KeyError:
                attempts = 0

            if level_mappings[act][level_id].get("is_boss"):
                name = name + Text(" (Boss)", style="magenta")

                if rank == "NotFinished":
                    rank = "Incomplete"
                else:
                    # RD doesn't give a rank to bosses, it just marks it as A if you've completed it
                    rank = "Completed"
            else:
                if rank == "NotFinished":
                    rank = "Unplayed"
                elif rank.startswith("C") or rank.startswith("D") or rank.startswith("F"):
                    rank = Text(rank, style="bright_black")
                elif rank.startswith("S"):
                    rank = Text(rank, style="yellow")
            
            if level_mappings[act][level_id].get("is_intermission"):
                name = name + Text(" (Intermission)", style="magenta")

            table.add_row(designator + " " + name, rank, str(attempts))

        print(table)


# for file in save_folder.iterdir():
#     print(file)

if __name__ == "__main__":
    for save_file in save_folder.glob("*.rdsave"):
        with save_file.open() as f:
            save = json.loads(
                f.read()[3:]
            )  # Saves begin with some unreadable characters
            saves[save_file.name.split(".")[0]] = save
            # print(json.dumps(save, sort_keys=True, indent=4))

    option, _ = pick.pick(
        ["Settings", "Slot 1", "Slot 2", "Slot 3"],
        "Select which save file you wish to browse:",
    )
    match option:
        case "Settings":
            walk_through_save(saves["settings"])
        case "Slot 1":
            walk_through_save(saves["slot0"])
        case "Slot 2":
            walk_through_save(saves["slot1"])
        case "Slot 3":
            walk_through_save(saves["slot2"])
