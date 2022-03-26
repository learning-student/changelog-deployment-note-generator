import json
import unittest
from os.path import dirname, join

from src.utils.changelog import generate_changelog, get_total_summary


class ChangeLogTest(unittest.TestCase):

    def test_summary_with_breaking_changes(self):
        changes = '{"feat":{"invitation":{"added_environments":["TEST_ENV", "ASASDADS"],"changed_environments":["BACKEND_URL"],"execute_commands":["php artisan migrate"],"all_commits":["fix(invitation): Fixed general commit"]}},"breaking":{"test":{"added_environments":["TEST_ENV"],"changed_environments":["BACKEND_URL"],"execute_commands":["php artisan migrate"],"all_commits":["breaking(invitation): Fixed general commit"]}}}'

        summary = get_total_summary(json.loads(changes))
        assert len(summary["breaking"]) == 1
        assert len(summary["added_environments"]) == 3
        assert len(summary["changed_environments"]) == 2
        assert len(summary["execute_commands"]) == 2
        assert len(summary["all_commits"]) == 2

    def test_changelog_generates_correctly_when_only_added_environments_given(self):
        def readLines():
            return [
                '{"feat":{"invitation":{"added_environments":["TEST_ENV"]}}}'
            ]

        changelog = generate_changelog(readLines)
        root_dir = dirname(dirname(__file__))
        test_md = join(root_dir, 'test.md')
        assert "#### INVITATION" in changelog
        assert "# Changelog" in changelog
        assert "###### New environment variables" in changelog
        assert "-`TEST_ENV`"
        with open(test_md, 'w+') as opened:
            opened.write(changelog)
            opened.close()

    def test_changelog_generates_correctly_when_details_not_required(self):
        def readLines():
            return [
                '{"feat":{"invitation":{"added_environments":["TEST_ENV"]}}}'
            ]

        changelog = generate_changelog(readLines, include_details=False)
        root_dir = dirname(dirname(__file__))
        test_md = join(root_dir, 'test.md')
        assert "#### INVITATION" not in changelog
        assert "# Changelog" in changelog
        assert "###### New environment variables" in changelog
        assert "-`TEST_ENV`"
        assert "Details" not in changelog
        with open(test_md, 'w+') as opened:
            opened.write(changelog)
            opened.close()
    def test_changelog_generates_correctly_when_all_data_given(self):
        def readLines():
            return [
                '{"feat":{"invitation":{"added_environments":["TEST_ENV"],"changed_environments":["BACKEND_URL"],"execute_commands":["php artisan migrate"],"all_commits":["fix(invitation): Fixed general commit"]}}}'
            ]

        changelog = generate_changelog(readLines)
        root_dir = dirname(dirname(__file__))
        test_md = join(root_dir, 'test.md')
        assert "#### INVITATION" in changelog
        assert "# Changelog" in changelog
        assert "###### New environment variables" in changelog
        assert "-`TEST_ENV`" in changelog
        assert "###### Changed environment variables" in changelog
        assert "-`BACKEND_URL`" in changelog
        assert "###### All commits" in changelog
        assert "-fix(invitation): Fixed general commit" in changelog

        with open(test_md, 'w+') as opened:
            opened.write(changelog)

    def test_changelog_generates_correctly_when_there_breaking_changes(self):
        changes = '{"feat":{"invitation":{"added_environments":["TEST_ENV", "ASASDADS"],"changed_environments":["BACKEND_URL"],"execute_commands":["php artisan migrate"],"all_commits":["fix(invitation): Fixed general commit"]}},"breaking":{"test":{"added_environments":["TEST_ENV"],"changed_environments":["BACKEND_URL"],"execute_commands":["php artisan migrate"],"all_commits":["breaking(invitation): Fixed general commit"]}}}'

        def readLines():
            return [
                changes
            ]

        changelog = generate_changelog(readLines)
        root_dir = dirname(dirname(__file__))
        test_md = join(root_dir, 'test.md')
        assert "#### INVITATION" in changelog
        assert "# Changelog" in changelog
        assert "###### New environment variables" in changelog
        assert "-`TEST_ENV`" in changelog
        assert "###### Changed environment variables" in changelog
        assert "-`BACKEND_URL`" in changelog
        assert "###### All commits" in changelog
        assert "-fix(invitation): Fixed general commit" in changelog

        with open(test_md, 'w+') as opened:
            opened.write(changelog)


if __name__ == '__main__':
    unittest.main()
