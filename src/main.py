from pick import pick

import core
import custom_levels
import story_mode

explorer_settings = {
    "Spoilers": False,
    "Save to file": False,
}


def generate_user_options(save_file: dict) -> list:
    input_options = []

    for setting in explorer_settings:
        if explorer_settings[setting]:
            input_options.append(f"{setting}: ON")
        else:
            input_options.append(f"{setting}: OFF")
    input_options.extend(save_file.keys())
    input_options.append("Exit")

    return input_options


if __name__ == "__main__":
    # 100% save file, for reference: https://steamcommunity.com/app/774181/discussions/0/693120275093500198/
    rd_saves = core.load_save_files()

    while True:
        option, _ = pick(
            generate_user_options(rd_saves),
            "Select which save file you wish to browse:",
        )

        if option == "Exit":
            break
        elif ":" in option:
            key, value = str(option).split(":")
            value = True if value == "ON" else False
            value = not value
            explorer_settings[key] = value
        elif option == "settings":
            custom_levels.walk_through_settings(rd_saves["settings"])
            break
        else:
            story_mode.walk_through_save(
                rd_saves[option],
                explorer_settings["Spoilers"],
                explorer_settings["Save to file"],
            )
            break
