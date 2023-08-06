import os
import yaml


def default_config():
    result = dict()
    result["changelog_file"] = "CHANGELOG.md"
    result["unreleased_changelog_entries_path"] = "./changelogs/unreleased"
    return result


class Config:
    def __init__(self, config_file_path: str):
        self.config = default_config()
        if os.path.isfile(config_file_path):
            self.config_file_path = config_file_path
            with open(self.config_file_path, "r") as file:
                self.config.update(yaml.load(file, Loader=yaml.FullLoader))

    def get_changelog_file(self):
        return self.__get_property("changelog_file")

    def get_issue_url(self):
        return self.__get_property("issue_url")

    def get_merge_request_url(self):
        return self.__get_property("merge_request_url")

    def get_unreleased_changelog_entries_path(self):
        return self.__get_property("unreleased_changelog_entries_path")

    def __get_property(self, property_name):
        if property_name in self.config:
            result = self.config[property_name]
        else:
            raise Exception(
                "Property '{}' is not defined in {}".format(
                    property_name,
                    self.config_file_path
                    if hasattr(self, "config_file_path")
                    else "default configuration",
                )
            )
        return result
