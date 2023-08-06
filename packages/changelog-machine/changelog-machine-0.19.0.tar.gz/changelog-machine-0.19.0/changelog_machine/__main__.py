import argparse
import sys

from changelog_machine.changelogGenerator import generate_changelog_cli
from changelog_machine.entryGenerator import generate_entry_cli


def main():
    parser = argparse.ArgumentParser(description="The machine to generate changelogs.")
    parser.add_argument("entry", help="To create an entry.", action="store_true")
    parser.add_argument(
        "changelog", help="To generate or append the changelog.", action="store_true"
    )

    arguments = sys.argv

    if len(arguments) < 2:
        parser.print_help()
    elif arguments[1] == "entry":
        generate_entry_cli()
    elif arguments[1] == "changelog":
        generate_changelog_cli()
    else:
        args = parser.parse_known_args()


if __name__ == "__main__":
    main()
