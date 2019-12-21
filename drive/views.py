from django.http import Http404
from django.shortcuts import render

from .models import Directory, File, NotFoundError


def index(request, path):
    path = path.split('/')
    try:
        directory = Directory.from_path(path)
        subdirs = directory.subdirectories()
        files = directory.files()
        context = {
            'path': path,
            'subdirs': subdirs,
            'files': files,
        }
        return render(request, 'drive/index.html', context)
    except NotFoundError:
        raise Http404("Directory not found")
