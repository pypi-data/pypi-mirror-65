import json
import os
import shutil

from mpp.src.utils import ask, constants as cst, files


def setup(args=None):
    """
    Asks information to the user and setup the environment

    Args:
        args (argparse args): parameters from parser.parse_args()
    """

    # Get information to forecast user's mpp_config
    current_dir = os.path.basename(os.getcwd())
    username = os.path.basename(os.path.expanduser("~"))

    # Ask questions
    mpp_config = dict()
    mpp_config["name"] = ask.question("What is your project name?", current_dir, required=True)
    mpp_config["author"] = ask.question("What is your author name?", username, required=True)
    mpp_config["version"] = "0.0.0"
    mpp_config["console"] = ask.question("Do you want to display the console (y/n)?", "y")
    mpp_config["console"] = mpp_config["console"].lower() == "y"
    mpp_config["icon"] = "resources/images/icon.ico"
    mpp_config["hidden-imports"] = list()

    # Create folders
    os.makedirs("installer", exist_ok=True)
    os.makedirs("resources/images", exist_ok=True)
    os.makedirs("src", exist_ok=True)

    # Add icon
    shutil.copy(cst.path_ico_default, mpp_config["icon"])

    files.write_mpp_config(mpp_config)

    # Write main file
    with open("main.py", "w") as f:
        f.write(cst.pattern_main_py % mpp_config)

    files.write_installer(mpp_config)

    print("")
    print(f"The project version is {mpp_config['version']}")
    print(f"The project's icon is here: {mpp_config['icon']}.")
    print("The `main.py` file can now be edited.")
    print("")
    print("Use `mpp --help` to display all possible commands")
    print("Use `mpp <command> -h` to display the help for a command.")
    print("Use `mpp config --list` to show your project settings.")
