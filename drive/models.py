from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name + '/'

    def subdirectories(self):
        """ Return a QuerySet of subdirectories. """
        return Directory.objects.filter(parent=self)

    def files(self):
        """ REturn a QuerySet of files inside the directory. """
        return File.objects.filter(parent=self)


class File(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)

    # path to the file's content as stored in the server's file system
    storage_name = models.CharField(max_length=255)

    @classmethod
    def upload():
        return cls()  # TODO

    def __str__(self):
        return self.name
