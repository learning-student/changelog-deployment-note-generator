from datetime import datetime
import json

from src.utils.markdown import markdown_title, markdown_code, markdown_list_item
from src.utils.mapping import type_mapping


def get_changelog_from_stdin(readLines):
    data = readLines()
    assert len(data) > 0
    return json.loads("".join(data))


def get_total_summary(changes):
    summary = {
        "breaking": [],
        "execute_commands": [],
        "added_environments": [],
        "changed_environments": [],
        "all_commits": []
    }

    for key, categories in dict(changes).items():

        for changelog in dict(categories).values():
            execute_commands = changelog['execute_commands'] if 'execute_commands' in changelog else []
            added_environments = changelog['added_environments'] if 'added_environments' in changelog else []
            changed_environments = changelog['changed_environments'] if 'changed_environments' in changelog else []
            all_commits = changelog['all_commits'] if 'all_commits' in changelog else []

            summary['execute_commands'] = [*summary['execute_commands'], *execute_commands]
            summary['added_environments'] = [*summary['added_environments'], *added_environments]
            summary['changed_environments'] = [*summary['changed_environments'], *changed_environments]
            summary['all_commits'] = [*summary['all_commits'], *all_commits]
            if key == 'breaking':
                summary['breaking'] = [*summary['breaking'], *all_commits]

    return summary

def render_list(data, title: str, key: str):
    changelog_text = ""
    list = data[key] if key in data else []
    if len(list) > 0:
        changelog_text += markdown_title(title, h=6)

        for item in list:
            changelog_text += markdown_list_item(markdown_code(item))

    return changelog_text

def generate_changelog(readLines, include_details : bool = True) -> str:
    changes = get_changelog_from_stdin(readLines)
    changelog_text = markdown_title('Changelog ' + datetime.today().strftime('%Y-%m-%d'))
    changelog_text += markdown_title('Summary', h=2)
    summary = get_total_summary(changes)
    changelog_text += "> There's been *{0}* commits since the last deploy".format(len(summary['all_commits']))

    if len(summary['breaking']) > 0:
        changelog_text += ", be **cautious** there are **{0}** BREAKING CHANGES".format(len(summary['breaking']))

    changelog_text += ".Developers added **{0}** new environment variables and changed **{1}** environment variables. \n".format(
        len(summary['added_environments']),
        len(summary['changed_environments'])
    )

    changelog_text += render_list(summary, 'Deployment Commands', 'execute_commands')
    changelog_text += render_list(summary, 'New environment variables', 'added_environments')
    changelog_text += render_list(summary, 'Changed environment variables', 'changed_environments')    

    if include_details is False:
        return changelog_text
    changelog_text += markdown_title('Details', h=2)

    changelog_text += "___ \n"
    for key, categories in changes.items():
        key = str(key)
        changelog_text += markdown_title(type_mapping[key] if key in type_mapping else str(key).upper(), h=3)
        for category, changelog in categories.items():
            changelog_text += markdown_title(str(category).upper(), h=4)

            changelog_text += render_list(changelog, 'Deployment Commands', 'execute_commands')
            changelog_text += render_list(changelog, 'New environment variables', 'added_environments')
            changelog_text += render_list(changelog, 'Changed environment variables', 'changed_environments')
            changelog_text += render_list(changelog, 'All commits"', 'all_commits')

    return changelog_text
