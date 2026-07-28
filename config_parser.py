from typing import TypedDict, Dict, Tuple
import os
from typing import Optional


class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    PERFECT: bool
    OUTPUT_FILE: str
    SEED: Optional[int]


def config_parser(filepath: str) -> MazeConfig:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: file with filepath"
                                f"{filepath} not found!")

    config_dict: Dict[str, str] = {}
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("Invalid syntax for config file, missing =")
            key, val = line.split("=")
            config_dict[key.strip().upper()] = val.strip()
        key_list = ["WIDTH", "HEIGHT", "ENTRY",
                    "EXIT", "PERFECT", "OUTPUT_FILE"]
        missing_keys = []
        for key in key_list:
            if key not in config_dict.keys():
                missing_keys.append(key)
        if missing_keys:
            missing_keys_str = ",".join(missing_keys)
            raise ValueError(f"Invalid syntax for config file:"
                             f"missing keys [{missing_keys_str}]")
        try:
            width = int(config_dict["WIDTH"])
            height = int(config_dict["HEIGHT"])
        except ValueError:
            raise ValueError("Width and height have to be integers")

        seed: Optional[int] = None
        if "SEED" in config_dict:
            try:
                seed = int(config_dict["SEED"])
            except ValueError:
                raise ValueError("SEED has to be an integer")

        try:
            entry_str = config_dict["ENTRY"].split(',')
            if len(entry_str) != 2:
                raise ValueError("ENTRY must be formatted as 'x,y'")
            entry_coords = (int(entry_str[0]), int(entry_str[1]))
            exit_str = config_dict["EXIT"].split(',')
            if len(exit_str) != 2:
                raise ValueError("EXIT must be formatted as 'x,y'")
            exit_coords = (int(exit_str[0]), int(exit_str[1]))
            perfect = config_dict["PERFECT"].lower()
            if perfect in ("true", "1", "yes"):
                perfect = True
            elif perfect in ("false", "0", "no"):
                perfect = False
            else:
                raise ValueError("PERFECT must be True or False")
            output_file = config_dict["OUTPUT_FILE"].strip()
            if not output_file:
                raise ValueError("Output file cannot be empty")
            if os.path.isdir(output_file):
                raise ValueError("Provided output file is a directory, "
                                 "it must be a file")
            parent_dir = os.path.dirname(output_file) or "."
            if not os.path.exists(parent_dir):
                raise ValueError(f"Destination directory '{parent_dir}'"
                                 f"does not exist")
        except ValueError as e:
            raise ValueError(f"Invalid syntax for config file: {e}")
        if width < 0 or height < 0:
            raise ValueError("Width and height values have to be positive")
        if entry_coords[0] < 0 or entry_coords[0] >= width:
            raise ValueError("Entry coordinate out of boundaries")
        if entry_coords[1] < 0 or entry_coords[1] >= height:
            raise ValueError("Entry coordinate out of boundaries")
        if exit_coords[0] < 0 or exit_coords[0] >= width:
            raise ValueError("Exit coordinate out of boundaries")
        if exit_coords[1] < 0 or exit_coords[1] >= height:
            raise ValueError("Exit coordinate out of boundaries")
        if entry_coords == exit_coords:
            raise ValueError("Entry and Exit coordinates cannot be the same")
    return {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry_coords,
        "EXIT": exit_coords,
        "PERFECT": perfect,
        "OUTPUT_FILE": output_file,
        "SEED": seed
        }


if __name__ == "__main__":
    import sys
    try:
        print(config_parser("/home/zscekic/core/a_maze_ing/config.txt"))
    except (FileNotFoundError, ValueError) as err:
        print(err, file=sys.stderr)
        sys.exit(1)
