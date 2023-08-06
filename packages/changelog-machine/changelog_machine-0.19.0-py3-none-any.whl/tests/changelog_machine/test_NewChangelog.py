from datetime import datetime

from changelog_machine.NewChangelog import render_entry, render_title


class Test:
    def test_render_entry_title_only(self):
        raw_content = {
            "title": "Title",
            "merge_request": None,
            "issue": None,
            "author": None,
        }

        result = render_entry("issue_url/{id}", "merge_request/{id}", raw_content)
        expected = "- Title."
        assert result == expected

    def test_render_entry_title_only_set(self):
        raw_content = {"title": "Title"}

        result = render_entry("issue_url/{id}", "merge_request/{id}", raw_content)
        expected = "- Title."
        assert result == expected

    def test_render_entry_title_with_dot(self):
        raw_content = {"title": "Title."}

        result = render_entry("issue_url/{id}", "merge_request/{id}", raw_content)
        expected = "- Title."
        assert result == expected

    def test_render_entry_all(self):
        raw_content = {
            "title": "Title",
            "merge_request": 12,
            "issue": 123,
            "author": "dev@foo.lu",
        }

        result = render_entry("issue_url/{id}", "merge_request/{id}", raw_content)
        expected = "- Title. [!12](merge_request/12) [#123](issue_url/123) dev@foo.lu"
        assert result == expected

    def test_render_title(self):

        result = render_title("1.2.3")
        expected = "## 1.2.3 ({})".format(datetime.today().strftime("%Y-%m-%d"))
        assert result == expected
