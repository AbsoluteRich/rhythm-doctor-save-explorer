from pathlib import Path

from rich.table import Table
from rich.text import Text

import core

OUTPUT_FOLDER = Path(Path.cwd() / "output")


def walk_through_save(
    save: dict, spoilers: bool = False, save_to_file: bool = False
) -> None:
    level_mappings = core.load_mappings()

    for act in level_mappings:
        table = Table(title=act)
        table.add_column("Level")
        table.add_column("Rank")
        table.add_column("Attempts")

        for level_id in level_mappings[act]:
            try:
                rank = save[f"Level_{level_id}_rank"]
            except KeyError:
                if not spoilers:
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

        if table.rows:
            core.console.print(table)

            if save_to_file:
                if not OUTPUT_FOLDER.exists():
                    OUTPUT_FOLDER.mkdir()

                with open(
                    OUTPUT_FOLDER / f"{table.title}.txt", "w", encoding="utf-8"
                ) as f:
                    f.write(core.console.export_text())
                print("Saved to file.")
