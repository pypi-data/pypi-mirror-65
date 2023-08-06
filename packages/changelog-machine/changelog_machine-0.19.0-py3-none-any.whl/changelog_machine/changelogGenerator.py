import argparse
import os
import re

from changelog_machine.Config import Config
from changelog_machine.NewChangelog import new_changelog, delete_unreleased_yaml
from changelog_machine.versions.VersionUtil import sort_versions


def generate_changelog_cli():
    parser = argparse.ArgumentParser(description="Create a changelog entry.")
    parser.add_argument(
        "changelog", help="To generate or append the changelog.", action="store_true"
    )
    parser.add_argument(
        "--releaseVersion", help="The version of the release", required=True
    )
    parser.add_argument(
        "--config",
        help="The config file (default: ./changelogs/config.yml)",
        default="./changelogs/config.yml",
    )

    args, unknown = parser.parse_known_args()
    config_path = args.config
    release_version = args.releaseVersion
    _generate_changelog(config_path, release_version)


def _generate_changelog(config_path: str, release_version: str):
    config = Config(config_path)

    changelog_file_name = config.get_changelog_file()

    print("Hello I will generate your changelog")
    if not os.path.isfile(changelog_file_name):
        print(
            "No '{}' found. I will generate an empty one for you...".format(
                changelog_file_name
            )
        )
        open(changelog_file_name, "w").close()
    with open(changelog_file_name, "r") as changelog_file:
        content = changelog_file.read()
    changelog = dict()
    changelog[release_version] = new_changelog(release_version, config)
    no_entry_content = ""
    current_version = None
    for line in content.split("\n"):
        version_search = re.search("^## (([0-9]+\\.?)+)", line, re.IGNORECASE)
        if version_search:
            current_version = version_search.group(1)
            changelog[current_version] = line
        elif current_version is not None:
            changelog[current_version] = "{}\n{}".format(
                changelog[current_version], line
            )
        else:
            no_entry_content = (
                "{}\n{}".format(no_entry_content, line) if no_entry_content else line
            )
    versions = sort_versions(changelog.keys())
    result = no_entry_content
    for v in versions:
        result = "{}\n{}".format(result, changelog[v])
    with open(changelog_file_name, "w") as changelog_file:
        changelog_file.write(result)
    delete_unreleased_yaml()
