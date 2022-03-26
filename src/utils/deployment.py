from datetime import datetime

from src.utils.changelog import get_changelog_from_stdin, get_total_summary, render_list
from src.utils.markdown import markdown_title


def generate_deployment_notes(readLines):
    summary = get_changelog_from_stdin(readLines)

    deployment_note_text = markdown_title('Deployment Notes ' + datetime.today().strftime('%Y-%m-%d'))

    deployment_note_text += render_list(summary, 'Deployment Commands', 'execute_commands')
    deployment_note_text += render_list(summary, 'New environment variables', 'added_environments')
    deployment_note_text += render_list(summary, 'Changed environment variables', 'changed_environments')

    return deployment_note_text


