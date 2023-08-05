import click
from .context_state import CliContextState


def quiet_mode_option(func):
    """
    Add quiet mode flag to context state

    Args:
        func:
    """
    def callback(ctx, _, value):
        state = ctx.ensure_object(CliContextState)
        state.quiet_mode = value
        return value
    return click.option('-q', '--quiet', default=False, is_flag=True, required=False, help='Run in quiet mode.',
                        expose_value=False, callback=callback)(func)


def common_options(func):
    """
    Adds common options used by multiple CLI commands

    Args:
        func:
    """
    func = quiet_mode_option(func)
    return func
