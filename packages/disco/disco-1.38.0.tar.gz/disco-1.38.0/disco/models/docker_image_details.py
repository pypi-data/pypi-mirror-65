from .base_model import BaseModel


class DockerImageDetails(BaseModel):
    """
    Docker image details.
    """

    def __init__(self, data, is_default_docker=False):
        super(DockerImageDetails, self).__init__(data)
        self._is_default = is_default_docker

    @property
    def is_default(self):
        """
        Returns: True if this is the default docker image
        """
        return self._is_default

    @property
    def id(self):
        """
        Returns:
            str
        """
        return self._data.get('id')

    @property
    def name(self):
        """
        Returns:
            str
        """
        return self._data.get('displayName')

    @property
    def repository_type(self):
        """
        Returns:
            str
        """
        return self._data.get('repositoryType')

    @property
    def path(self):
        """
        Returns:
            str
        """
        return self._data.get('path')

    @property
    def entry_point(self):
        """
        Returns:
            str
        """
        return self._data.get('entryPoint')

    @property
    def is_active(self):
        """
        Returns:
            str
        """
        return self._data.get('isActive')
