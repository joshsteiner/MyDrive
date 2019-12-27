from django.db import models
from django.core.validators import MinLengthValidator, ValidationError


class NotFoundError(Exception):
    """ Raised when a directory or file was not found at
        the requested location.
    """
    pass


class Directory(models.Model):
    ROOT = None

    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(1)])
    parent = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('parent', 'name')

    def __str__(self):
        return self.name + '/'

    @staticmethod
    def remove(path):
        """ Remove directory. """
        Directory.from_path(path).delete()

    @staticmethod
    def make(path):
        """ Make directory. """
        pass

    @staticmethod
    def subdirs(directory):
        """ Return a QuerySet of subdirectories. """
        return Directory.objects.filter(parent=directory)

    @staticmethod
    def files(directory):
        """ Return a QuerySet of files inside the directory. """
        return File.objects.filter(directory=directory)

    @classmethod
    def from_path(cls, path):
        """ Get directory at specified path.
            Raise NotFoundError if not found.
        """
        directory = None
        for dirname in path:
            directory = Directory.objects \
                .filter(parent=directory, name=dirname) \
                .first()
            if directory is None:
                raise NotFoundError()
        return directory


class File(models.Model):
    directory = models.ForeignKey(
        Directory,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(
        max_length=256,
        validators=[MinLengthValidator(1)])
    size = models.IntegerField(
        default=0)

    # path to the file's content as stored in the server's file system
    # NOTE: null, blank is temporary
    storage_name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        unique_together = ('directory', 'name')

    def __str__(self):
        return self.name

    @classmethod
    def from_path(cls, path):
        """ Get file at specified path.
            Raise NotFoundError if not found.
        """
        directory = Directory.from_path(path[:-1])
        file_ = File.objects.filter(directory=directory, name=path[-1]).first()
        if file_ is None:
            raise NotFoundError()
        return file_
