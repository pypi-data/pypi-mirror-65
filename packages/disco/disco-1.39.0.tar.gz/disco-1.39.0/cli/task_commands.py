import click

import moment
from cli.command_utils import info_message, exception_message, list_to_table, verify_logged_in
from disco import Task
from disco.core.exceptions import DiscoException

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group('task', context_settings=CONTEXT_SETTINGS)
def task_commands():
    """Manage tasks."""


@task_commands.command('show', context_settings=CONTEXT_SETTINGS,
                       short_help="Gets the activity log of the task.")
@click.argument('task_id', metavar='<TASK_ID>')
def show(task_id):
    """
    Gets the activity log of the task.

    $ disco task show <TASK_ID>
    """
    if not verify_logged_in():
        return

    try:
        task = Task(task_id)
        task_events = task.get_task_events_log()
        if len(task_events) > 0:
            display_task_events(task_events)
        else:
            info_message('No logs available yet.')
    except DiscoException as ex:
        exception_message(ex)


def display_task_events(task_events):
    """Receives a list of tasks events and prints them as a table"""
    tabulated_array = []
    for task_event in task_events:
        time = moment.date(task_event.time).locale().date.strftime("%m/%d/%Y %H:%M:%S")
        tabulated_array.append([time, task_event.display_message])
    displayable_table = list_to_table(tabulated_array, ["Date", "Event"])
    info_message(displayable_table)
