from .base_model import BaseModel


class TaskAuditEvent(BaseModel):
    """
    Task audit events details
    """

    @property
    def time(self):
        """
        Returns:
            str
        """
        return self._data.get('time')

    @property
    def display_message(self):
        """
        Returns:
            str
        """
        return self._data.get('displayMessage')

    @property
    def type(self):
        """
        Returns:
            str
        """
        return self._data.get('type')
