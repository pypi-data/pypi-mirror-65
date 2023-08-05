import click


class CliContextState:
    """
    CLI Context State
    """

    def __init__(self, quiet_mode=False):
        """
        Args:
            quiet_mode (bool): Run in quiet mode
        """
        self.quiet_mode = quiet_mode


pass_state = click.make_pass_decorator(CliContextState, ensure=True)  # pylint: disable=invalid-name
