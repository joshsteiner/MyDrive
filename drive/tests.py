from django.test import TestCase

from .models import Directory, File, NotFoundError


class DirectoryModelTest(TestCase):

    def test_make_directory_list_subdirectories(self):
        """ After making a directory with a parent,
            the parent and child are connected.
        """
        parent = Directory(name='parent')
        child = Directory(name='child', parent=parent)
        parent.save()
        child.save()
        self.assertQuerysetEqual(
            parent.subdirectories(),
            {'<Directory: child/>'}
        )

    def test_make_file_list_files(self):
        """ Create files and add to parent, assert connected. """
        directory = Directory(name='directory')
        directory.save()
        File(name='file1', directory=directory).save()
        File(name='file2', directory=directory).save()
        self.assertQuerysetEqual(
            directory.files(),
            {'<File: file1>', '<File: file2>'},
            ordered=False
        )

    def test_from_path(self):
        """ Get directory using from_path(). """
        a = Directory(name='a')
        b = Directory(name='b', parent=a)
        c = Directory(name='c', parent=b)
        a.save()
        b.save()
        c.save()
        self.assertEqual(Directory.from_path('a'), a)
        self.assertEqual(Directory.from_path('a/b'), b)
        self.assertEqual(Directory.from_path('a/b/c'), c)

    def test_from_path_when_no_dir(self):
        """ Get directory using from_path() when directory doesn't exist. """
        a = Directory(name='a')
        b = Directory(name='b', parent=a)
        c = Directory(name='c', parent=b)
        a.save()
        b.save()
        c.save()
        with self.assertRaises(NotFoundError):
            Directory.from_path('r')
        with self.assertRaises(NotFoundError):
            Directory.from_path('b')
        with self.assertRaises(NotFoundError):
            Directory.from_path('a/c')


class FileModelTest(TestCase):

    def setUp(self):
        """ Create directories and files used for tests """
        self.d = Directory(name='d')
        self.f = File(name='f', directory=self.d)
        self.d.save()
        self.f.save()

    def test_from_path(self):
        """ Get file using from_path(). """
        self.assertEqual(File.from_path('d/f'), self.f)

    def test_from_path_when_no_dir(self):
        """ Get file using from_path() when no directory. """
        with self.assertRaises(NotFoundError):
            File.from_path('r/f')

    def test_from_path_when_no_file(self):
        """ Get file using from_path() when file doesn't exist. """
        with self.assertRaises(NotFoundError):
            File.from_path('d/f2')
