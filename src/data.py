from rich.console import Console

console = Console()
print = console.print

# Abomination
level_mappings = {
    "Act 1": {
        # theme of really spooky bird will be added when I get it in my save file
        "OrientalTechno": {"designator": "1-1", "name": "Samurai Techno"},
        "Intimate": {"designator": "1-2", "name": "Intimate"},
        "OrientalInsomniac": {
            "designator": "1-X",
            "name": "Battleworn Insomniac",
            "is_boss": True,
        },
        "GongXi": {"designator": "1-CNY", "name": "Chinese New Year"},
        "OrientalDubstep": {"designator": "1-1N", "name": "Samurai Dubstep"},
        "IntimateH": {"designator": "1-2N", "name": "Intimate (Night)"},
        "InsomniacHard": {
            "designator": "1-XN",
            "name": "Super Battleworn Insomniac",
            "is_boss": True,
        },
    },
    "Act 2": {
        "Lofi": {
            "designator": "2-1",
            "name": "Lo-fi Hip-Hop Beats To Treat Patients To",
        },
        "SVT": {
            "designator": "2-2",
            "name": "Supraventricular Tachycardia",
        },
        "Smokin": {
            "designator": "2-3",
            "name": "Puff Piece",
        },
        "SongOfTheSea": {
            "designator": "2-4",
            "name": "Song of the Sea",
            "is_intermission": True,
        },
        "Boss2": {
            "designator": "2-X",
            "name": "All The Times",
            "is_boss": True,
        },
        "BeansHopper": {
            "designator": "2-B1",
            "name": "Beans Hopper",
        },
    },
}


if __name__ == "__main__":
    # Generates the schema
    for act in range(1, 7 + 1):
        level_mappings[f"Act {act}"] = {
            "id": {"designator": None, "name": None, "is_boss": False}
        }

    print(level_mappings)
