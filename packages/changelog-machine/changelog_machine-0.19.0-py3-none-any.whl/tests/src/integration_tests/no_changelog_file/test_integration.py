import os

from changelog_machine.changelogGenerator import _generate_changelog
from changelog_machine.entryGenerator import _generate_entry


def content_of_setup(path):
    with open("{}/setup/{}".format(os.path.dirname(__file__), path)) as f:
        return f.read()


def content_matches_expected(tmpdir):
    for (dirpath, dirnames, filenames) in os.walk(
        "{}/expected".format(os.path.dirname(__file__))
    ):
        for file_name in filenames:
            with open("{}/{}".format(dirpath, file_name)) as expected_file:
                expected = expected_file.read()
            with open("{}/{}".format(tmpdir, file_name)) as expected_file:
                result = expected_file.read()
            assert expected == result


def test_no_changelog_file(tmpdir):
    changelogs_dir = tmpdir.mkdir("changelogs")
    config_file = changelogs_dir.join("config.yml")
    config_file.write(
        "{}\n{}\n{}".format(
            content_of_setup("changelogs/config.yml"),
            "changelog_file: '{}/CHANGELOG.md'".format(tmpdir),
            "unreleased_changelog_entries_path: '{}/changelogs/unreleased'".format(
                tmpdir
            ),
        )
    )
    unreleased_dir = changelogs_dir.mkdir("unreleased")

    _generate_entry("author", unreleased_dir, 123, 124, "Message")
    _generate_changelog(config_file, "1.1.0")

    content_matches_expected(tmpdir)
