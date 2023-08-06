import argparse
import re
import os

from changelog_machine.Config import Config


def generate_entry_cli():
    parser = argparse.ArgumentParser(description="Create a changelog entry.")
    parser.add_argument("entry", help="To create an entry.", action="store_true")
    parser.add_argument(
        "-i", "--issue-id", help="The issue id without the #", default=""
    )
    parser.add_argument(
        "-mr", "--merge-request", help="The merge request id", default=""
    )
    parser.add_argument("-a", "--author", help="The author of the change", default="")
    parser.add_argument(
        "-m", "--message", help="The message of the entry", required=True
    )
    parser.add_argument(
        "--config",
        help="The config file (default: ./changelogs/config.yml)",
        default="./changelogs/config.yml",
    )

    args, unknown = parser.parse_known_args()

    config = Config(args.config)

    message = args.message
    merge_request = args.merge_request
    issue_id = args.issue_id
    author = args.author
    directory = config.get_unreleased_changelog_entries_path()

    _generate_entry(author, directory, issue_id, merge_request, message)


def _generate_entry(author, directory, issue_id, merge_request, message):
    entry = """---
title: '{}'
merge_request: {}
issue: {}
author: '{}'
""".format(
        message, merge_request, issue_id, author
    )
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = "{}/{}.yml".format(directory, re.sub("[^0-9a-zA-Z]+", "_", message))
    index = 0
    while os.path.isfile(filename):
        filename = "{}/{}.yml".format(
            directory, re.sub("[^0-9a-zA-Z]+", "_", message + "_" + str(index))
        )
        index = index + 1
    with open(filename, "w") as out:
        out.write(entry)
