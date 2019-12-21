from django.test import TestCase, Client
from django.core.validators import ValidationError
from django.urls import reverse

from .models import Directory, File, NotFoundError


class DirectoryModelTests(TestCase):

    def setUp(self):
        """ Create directories and files used for tests. """
        self.a = Directory(name='a', parent=Directory.ROOT)
        self.b = Directory(name='b', parent=Directory.ROOT)
        self.a_c = Directory(name='c', parent=self.a)
        self.a_b = Directory(name='b', parent=self.a)
        self.a_c_d = Directory(name='d', parent=self.a_c)
        self.f1 = File(name='f1', directory=Directory.ROOT)
        self.f2 = File(name='f2', directory=Directory.ROOT)
        self.a.save()
        self.b.save()
        self.a_c.save()
        self.a_b.save()
        self.a_c_d.save()
        self.f1.save()
        self.f2.save()

    def test_subdirs(self):
        """ Get subdirs using `subdirectories()`. """
        self.assertQuerysetEqual(
            Directory.subdirs(self.a),
            {repr(self.a_b), repr(self.a_c)},
            ordered=False
        )

    def test_files(self):
        """ Get files using `files()`. """
        self.assertQuerysetEqual(
            Directory.files(Directory.ROOT),
            {repr(self.f1), repr(self.f2)},
            ordered=False
        )

    def test_from_path(self):
        """ Get directory using from_path(). """
        self.assertEqual(Directory.from_path(['a', 'b']), self.a_b)

    def test_from_path_when_no_dir(self):
        """ Get directory using from_path() when directory doesn't exist. """
        with self.assertRaises(NotFoundError):
            Directory.from_path(['a', 'r'])

    def test_from_path_root(self):
        """ Get root folder using from_path(). """
        self.assertEqual(Directory.from_path([]), Directory.ROOT)

    def test_create_dir_when_name_empty(self):
        """ Create directory when name is an empty string.
            Should raise exception.
        """
        with self.assertRaises(ValidationError):
            d = Directory(name='')
            d.full_clean()
            d.save()

    def test_create_duplicate_dir(self):
        """ Create multiple dirs with the same name in the same dir.
            Should raise exception.
        """
        with self.assertRaises(ValidationError):
            d = Directory(name='c', parent=self.a)
            d.full_clean()
            d.save()


class FileModelTests(TestCase):

    def setUp(self):
        """ Create directories and files used for tests """
        self.d = Directory(name='d')
        self.f = File(name='f', directory=self.d)
        self.d.save()
        self.f.save()

    def test_from_path(self):
        """ Get file using from_path(). """
        self.assertEqual(File.from_path(['d', 'f']), self.f)

    def test_from_path_when_no_dir(self):
        """ Get file using from_path() when no directory. """
        with self.assertRaises(NotFoundError):
            File.from_path(['r', 'f'])

    def test_from_path_when_no_file(self):
        """ Get file using from_path() when file doesn't exist. """
        with self.assertRaises(NotFoundError):
            File.from_path(['d', 'f2'])

    def test_create_file_when_name_empty(self):
        """ Create file when name is an empty string.
            Should raise exception.
        """
        with self.assertRaises(ValidationError):
            f = File(name='')
            f.full_clean()
            f.save()

    def test_create_duplicate_file(self):
        """ Create multiple files with the same name in the same dir.
            Should raise exception.
        """
        with self.assertRaises(ValidationError):
            f = File(name='f', directory=self.d)
            f.full_clean()
            f.save()
