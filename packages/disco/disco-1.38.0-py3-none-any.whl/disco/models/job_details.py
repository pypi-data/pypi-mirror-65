from disco.core.constants import JobStatus
from .base_model import BaseModel


class JobDetails(BaseModel):
    """
    Job Details
    """

    @property
    def id(self):
        """
        Returns:
            str
        """
        return self._data.get('id')

    @property
    def status(self):
        """
        Returns:
            str
        """
        cur_status = self._data.get('status')
        return JobStatus.done.value if cur_status == JobStatus.stopped.value else cur_status

    @property
    def stopped(self):
        """
        Returns:
            boolean
        """
        return self._data.get('status') == JobStatus.stopped.value

    @property
    def archived(self):
        """
        Returns:
            str
        """
        return self._data.get('archived')

    @property
    def name(self):
        """
        Returns:
            str
        """
        return self._data.get('request', {}).get('meta', {}).get('name')

    @property
    def tasks_summary(self):
        """
        Returns:
            TasksSummary
        """
        summary_data = self._data.get('tasksSummary')
        if not summary_data:
            return None

        return TasksSummary(**summary_data)


class TasksSummary:  #pylint: disable=redefined-builtin,too-many-instance-attributes
    """
    Tasks Summary
    """

    # pylint: disable=too-many-arguments
    def __init__(self, queued=0, running=0, failed=0, success=0, stopped=0, timeout=0, all=0):
        self.queued = queued
        self.running = running
        self.failed = failed
        self.success = success
        self.stopped = stopped
        self.timeout = timeout
        self.all = all
