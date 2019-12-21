from django.http import Http404
from django.shortcuts import render

from .models import Directory, File, NotFoundError


def root(request):
    return index(request, '')


def index(request, path):
    path = _split_path(path)
    try:
        directory = Directory.from_path(path)
        subdirs = Directory.subdirs(directory)
        files = Directory.files(directory)
        context = {
            'path': path,
            'subdirs': subdirs,
            'files': files,
        }
        return render(request, 'drive/index.html', context)
    except NotFoundError:
        raise Http404("Directory not found")


def _split_path(path):
    if path == '':
        return []
    else:
        return path.split('/')
