from django.db import models


class NotFoundError(Exception):
    """ Raised when a directory or file was not found at
        the requested location.
    """
    pass


class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name + '/'

    def subdirectories(self):
        """ Return a QuerySet of subdirectories. """
        return Directory.objects.filter(parent=self)

    def files(self):
        """ Return a QuerySet of files inside the directory. """
        return File.objects.filter(directory=self)

    @classmethod
    def from_path(cls, path):
        """ Get directory at specified path.
            Raise NotFoundError if not found.
        """
        directory = None
        for dirname in path.split('/'):
            directory = Directory.objects \
                .filter(parent=directory, name=dirname) \
                .first()
            if directory is None:
                raise NotFoundError()
        return directory


class File(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=256)
    size = models.IntegerField(default=0)

    # path to the file's content as stored in the server's file system
    storage_name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    @classmethod
    def from_path(cls, path):
        """ Get file at specified path.
            Raise NotFoundError if not found.
        """
        path = path.split('/')
        filename = path[-1]
        dirname = '/'.join(path[:-1])
        directory = Directory.from_path(dirname)
        file_ = File.objects.filter(directory=directory, name=filename).first()
        if file_ is None:
            raise NotFoundError()
        return file_
