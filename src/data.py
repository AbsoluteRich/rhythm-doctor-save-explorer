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
            "is_bonus": True,
        },
        "CareLess": {
            "designator": "2-1N",
            "name": "wish i could care less",
        },
        "Unreachable": {
            "designator": "2-2N",
            "name": "Unreachable",
        },
        "Pomeranian": {
            "designator": "2-3N",
            "name": "Bomb-Sniffing Pomeranian",
        },
        "SongOfTheSeaH": {
            "designator": "2-4N",
            "name": "Song of the Sea (Night)",
            "is_intermission": True,
        },
        "Bitterness": {
            "designator": "2-XN",
            "name": "Bitter Times",
            "is_boss": True,
        },
    },
    "Act 3": {
        "Garden": {
            "designator": "3-1",
            "name": "Sleepy Garden",
        },
        "Classy": {
            "designator": "3-2",
            "name": "Classy",
        },
        "DistantDuet": {
            "designator": "3-3",
            "name": "Distant Duet",
        },
        "Lesmis": {
            "designator": "3-X",
            "name": "One Shift More",
            "is_boss": True,
        },
        # Rhythm Dogtor
        "Lounge": {
            "designator": "3-1N",
            "name": "Lounge",
        },
        "ClassyH": {
            "designator": "3-2N",
            "name": "Classy (Night)",
        },
        "DistantDuetH": {
            "designator": "3-3N",
            "name": "Distant Duet (Night)",
        },
        # Unused: See https://wiki.rhythm.cafe/page/G_And_Tonic
        # "GAndTonic": {
        #     "designator": "3-B1",
        #     "name": "G And Tonic",
        #     "is_bonus": True,
        # }
    },
    "Act 4": {
        "Heldbeats": {
            "designator": "4-1",
            "name": "Training Doctor's Train Ride Performance",
        },
        "Invisible": {
            "designator": "4-2",
            "name": "Invisible",
        },
        "Steinway": {
            "designator": "4-3",
            "name": "Steinway",
        },
        "KnowYou": {
            "designator": "4-4",
            "name": "Know You",
        },
        "Rollerdisco": {
            "designator": "4-1N",
            "name": "Rollerdisco Rumble",
        },
        "InvisibleH": {
            "designator": "4-2N",
            "name": "Invisible (Night)",
        },
        "SteinwayH": {
            "designator": "4-3N",
            "name": "Steinway Reprise",
        },
        "Murmurs": {
            "designator": "4-4N",
            "name": "Murmurs",
        },
    },
    "Act 5": {
        "LuckyBreak": {
            "designator": "5-1",
            "name": "Lucky Break",
        },
        "Freezeshot": {
            "designator": "5-2",
            "name": "Lo-fi Beats For Patients To Chill To",
        },
        "AthleteTherapy": {
            "designator": "5-3",
            "name": "Seventh-Inning Stretch",
            "is_intermission": True,
        },
        "RhythmWeightlifter": {
            "designator": "5-B1",
            "name": "Rhythm Weightlifter",
            "is_bonus": True,
        },
        "AthleteFinale": {
            "designator": "5-X",
            "name": "Dreams Don't Stop",
            "is_boss": True,
        },
        "Injury": {
            "designator": "5-1N",
            "name": "One Slip Too Late",
        },
        "FreezeshotH": {
            "designator": "5-2N",
            "name": "Unsustainable Inconsolable",
        },
        "StevensonsTango": {
            "designator": "5-3N",
            "name": "Corazones Viejos",
        },
    },
    "Act 6": {
        "HaileyDuet": {
            "designator": "6-1",
            "name": "Something to Tell You",
        },
        "EdegaRave": {
            "designator": "6-2",
            "name": "Welcome Back",
        },
        "PaigesReckoning": {
            "designator": "6-3",
            "name": "Boss Fight",
            "is_boss": True,
        },
    },
    "Act 7": {
        "Blurred": {
            "designator": "7-1",
            "name": "Blurred",
        },
        "Montage": {
            "designator": "7-X",
            "name": "Miracle Defibrillator",
            "is_boss": True,
        },
        "Montage2": {
            "designator": "7-X2",
            "name": "Miracle Defibrillator (Cole's Song)",
            "is_boss": True,
        },
    },
    "Art Room": {
        "HelpingHands": {
            "designator": "X-0",
            "name": "Helping Hands",
        },
        "ArtExercise": {
            "designator": "X-1",
            "name": "Art Exercise",
        },
    },
    "Basement": {
        "MeetAndTweet": {
            "designator": "X-MAT",
            "name": "Meet and Tweet",
        },
        "Unbeatable": {
            "designator": "X-WOT",
            "name": "Worn Out Tapes",
        },
        "SparkLine": {
            "designator": "X-KOB",
            "name": "Kingdom of Balloons",
        },
        "VividStasis": {"designator": "X-FTS", "name": "Fixations Toward the Stars"},
    },
    "Muse Dash Collab": {
        "BlackestLuxuryCar": {
            "designator": "MD-1",
            "name": "Blackest Luxury Car",
        },
        "TapeStopNight": {
            "designator": "MD-2",
            "name": "tape/stop/night",
        },
        "The90sDecision": {
            "designator": "MD-3",
            "name": "The 90's Decision",
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
