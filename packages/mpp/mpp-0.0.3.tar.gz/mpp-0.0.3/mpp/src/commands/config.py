import json
import os
import shutil
import sys
import textwrap

from mpp.src.utils import ask, constants as cst, files


def config(args=None):
    """
    Show or edit configuration parameters

    Args:
        args (argparse args): parameters from parser.parse_args()
    """

    if not any([args.list, args.parameters]):
        print("This command needs parameters.")
        print("Use `mpp config --help` to show the help.")
        sys.exit()

    # Get project config file
    if not os.path.exists(".mpp_config"):
        sys.exit("Please setup your environment by using the 'setup' command")
    with open(".mpp_config") as f:
        mpp_config = json.load(f)

    # If there is no parameter
    if args.list:
        __show_config(mpp_config)
        sys.exit()

    # If there are parameters
    for param in args.parameters:
        if param not in mpp_config:
            valid = [f"'{x}'" for x in mpp_config.keys()]
            valid = ", ".join(valid)
            sys.exit(f"Invalid parameter: '{param}' (choose from {valid})")

    new_config = __process_parameters(args, mpp_config)
    if new_config:
        mpp_config.update(**new_config)
        files.write_mpp_config(mpp_config)
        files.write_installer(mpp_config)


def __show_config(mpp_config):
    """
    Shows the parameters from the configurtion file

    Args:
        mpp_config (dict): project parameters
    """

    values = [f" -→ {k} = {v}" for k, v in mpp_config.items()]
    print(*values, sep="\n")


def __process_parameters(args, mpp_config):
    """
    Processes the given parameters

    Args:
        args (argparse args): parameters from parser.parse_args()
        mpp_config (dict): project parameters

    Returns:
        dict: user's answers
    """

    # Process each parameter
    answers = dict()
    if "name" in args.parameters:
        answers["name"] = ask.question(
            "What is your project name?",
            default=mpp_config["name"]
        )
    if "author" in args.parameters:
        answers["author"] = ask.question(
            "What is your author name?",
            default=mpp_config["author"]
        )
    if "version" in args.parameters:
        answers["version"] = ask.question(
            "What is the new version?",
            default=mpp_config["version"]
        )
    if "console" in args.parameters:
        answers["console"] = ask.question(
            "Do you want to display the console (y/n)?",
            default="y" if mpp_config["console"] else "n"
        )
        answers["console"] = answers["console"].lower() == "y"
    if "hidden-imports" in args.parameters:
        answers["hidden-imports"] = __process_hidden_imports(mpp_config)

    # Validate modifications
    print("")
    is_ok = ask.question(
        "Are you sure of your modifications (y/n)?",
        required=True
    ).lower() == "y"

    if not is_ok:
        answers.clear()

    return answers


def __process_hidden_imports(mpp_config):
    """
    Processes the `hidden-imports` parameter

    Args:
        mpp_config (dict): project parameters

    Returns:
        list: user's hidden-imports
    """

    imports = mpp_config["hidden-imports"][:]
    help_msg = textwrap.dedent("""\
    Use `-<package>` to remove a package or `+<package>` to add it.
    Use `list` to display the current imports.
    Use `clear` to remove all the packages.
    Use `help` to show this message.
    Use `q` to exit.""")

    print("List of current hidden imports:")
    print(f"[{', '.join(imports)}]")
    print("")
    print(help_msg)

    while True:
        answer = input("> ")

        # Verify input
        if len(answer.split()) > 1:
            print("White spaces are not allowed.")
            continue

        # Exit
        if answer == "q":
            break
        # Show help
        elif answer == "help":
            print(help_msg)
        # Remove all
        elif answer == "clear":
            imports.clear()
        # Display list of imports
        elif answer == "list":
            print(f"[{', '.join(imports)}]")
        # Remove one package
        elif answer.startswith("-"):
            try:
                imports.remove(answer[1:])
            except ValueError:
                print(f"`{answer[1:]}` is not part of the hidden imports.")
        # Add one package
        elif answer.startswith("+"):
            imports.append(answer[1:])
        # Something else
        else:
            print(f"`{answer}` is not a valid entry")

    return sorted(set(imports))
