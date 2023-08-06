import os
from datetime import datetime
from os import walk

import yaml

from changelog_machine.Config import Config


def render_title(version):
    today = datetime.today().strftime("%Y-%m-%d")
    return "## {} ({})".format(version, today)


def new_changelog(version, config: Config):
    unreleased_changelog_entries_path = config.get_unreleased_changelog_entries_path()
    mr_base_url = config.get_merge_request_url()
    issue_base_url = config.get_issue_url()
    entries = ""
    for (dirpath, dirnames, filenames) in walk(unreleased_changelog_entries_path):
        for file_name in filenames:
            if file_name.endswith(".yml"):
                file_path = "{}/{}".format(dirpath, file_name)
                with open(file_path, "r") as file:
                    raw_content = yaml.load(file, Loader=yaml.FullLoader)
                    entry = render_entry(issue_base_url, mr_base_url, raw_content)
                    entries = "{}\n{}".format(entries, entry) if entries else entry
    if not entries:
        entries = "- No changes."
    title = render_title(version)
    result = """{}

{}
""".format(
        title, entries
    )

    print(result)
    return result


def render_entry(issue_base_url, mr_base_url, raw_content):
    result = "- {}".format(raw_content["title"])
    if not result.endswith("."):
        result = result + "."
    if "merge_request" in raw_content and raw_content["merge_request"]:
        mr_url = mr_base_url.replace("{id}", str(raw_content["merge_request"]))
        result = result + " [!{}]({})".format(raw_content["merge_request"], mr_url)
    if "issue" in raw_content and raw_content["issue"]:
        issue_url = issue_base_url.replace("{id}", str(raw_content["issue"]))
        result = result + " [#{}]({})".format(raw_content["issue"], issue_url)
    if "author" in raw_content and raw_content["author"]:
        result = result + " {}".format(raw_content["author"])
    return result


def delete_unreleased_yaml():
    changelog_entries_path = "changelogs/unreleased"
    for (dirpath, dirnames, filenames) in walk(changelog_entries_path):
        for file_name in filenames:
            if file_name.endswith(".yml"):
                file_path = "{}/{}".format(dirpath, file_name)
                os.remove(file_path)
