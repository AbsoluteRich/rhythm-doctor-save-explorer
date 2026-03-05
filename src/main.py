import json
import os
import pathlib

import json5
import pick
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
print = console.print


# Todo
def walk_through_settings(rd_save: dict):
    # https://discord.com/channels/296802696243970049/298297906509774848/1287309972018827397
    # it's author + artist + song through md5
    table = Table("Custom Levels")
    print(table)


def walk_through_save(rd_save: dict):
    # console.rule("Act 1")

    for act in level_mappings:
        table = Table(title=act)
        table.add_column("Level")
        table.add_column("Rank")
        table.add_column("Attempts")  # Not implemented yet

        for level_id in level_mappings[act]:
            try:
                rank = rd_save[f"Level_{level_id}_rank"]
                # del rd_save[f"Level_{level_id}_rank"]  # Debug
            except KeyError:
                table.add_row("???", "Unplayed", "0")
                continue

            designator = Text(
                level_mappings[act][level_id]["designator"], style="bright_green"
            )  # Close enough to lime
            name = Text(level_mappings[act][level_id]["name"], style="bright_cyan")

            try:
                attempts = rd_save[f"{level_id}_tries"]
                # del rd_save[f"{level_id}_tries"]  # Debug
            except KeyError:
                attempts = 0
            attempts = str(attempts)

            if level_mappings[act][level_id].get("is_boss"):
                # Todo: Text styling for perfect bosses, which means I need to beat one first :(
                # Also completed w/o checkpoints is a completely separate thing?? How many boss ranks are there
                name = name + Text(" (Boss)", style="magenta")

                if rank == "NotFinished":
                    rank = "Incomplete"
                elif rank == "A":
                    # RD doesn't give a rank to bosses, it just marks it as A if you've completed it
                    rank = "Completed"
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
    # print(sorted(rd_save.keys()))  # Debug


# for file in save_folder.iterdir():
#     print(file)

if __name__ == "__main__":
    for save_file in save_folder.glob("*.rdsave"):
        with save_file.open() as f:
            save = json.loads(f.read()[3:])

            saves[save_file.name.split(".")[0]] = save
            # print(json.dumps(save, sort_keys=True, indent=4))

    option, _ = pick.pick(
        ["Settings", "Slot 1", "Slot 2", "Slot 3"],
        "Select which save file you wish to browse:",
    )
    match option:
        case "Settings":
            walk_through_settings(saves["settings"])
        case "Slot 1":
            walk_through_save(saves["slot0"])
        case "Slot 2":
            walk_through_save(saves["slot1"])
        case "Slot 3":
            walk_through_save(saves["slot2"])
