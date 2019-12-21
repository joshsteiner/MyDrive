from django.http import Http404
from django.shortcuts import render

from .models import Directory, File, NotFoundError


def index(request, path):
    dirname = path
    try:
        directory = Directory.from_path(path)
        subdirs = directory.subdirectories()
        files = directory.files()
        context = {
            'dirname': dirname,
            'subdirs': subdirs,
            'files': files,
        }
        return render(request, 'drive/index.html', context)
    except NotFoundError:
        raise Http404("Directory not found")
