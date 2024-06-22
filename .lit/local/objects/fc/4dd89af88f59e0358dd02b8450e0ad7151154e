import argparse
import sys

from loguru import logger

from lit import run


def main():
    parser = argparse.ArgumentParser(description="Lit version control system.")
    parser.add_argument("command", metavar="command", type=str, help="Please enter the lit command you wish to use.")
    parser.add_argument("--m", help="Message argument for commits.")

    arguments = parser.parse_args()
    args_dict = vars(arguments)  # Convert arguments to dictionary
    args_dict = {k: v for k, v in args_dict.items() if v is not None}
    command = args_dict.pop("command", None)  # Remove 'command' key

    logger.info(f"Running command: {command}")
    if args_dict:
        run.run(command, args_dict)
    else:
        run.run(command)


if __name__ == "__main__":
    main()
