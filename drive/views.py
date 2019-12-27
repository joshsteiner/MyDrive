from django.http import Http404, JsonResponse
from django.shortcuts import render

from . import fsop
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


def file_system_op(request):
    """ Handle file system commands.

        ls - list directories and files

        mkdir - make directory
        rmdir - remove directory
        updir - upload directory
        downdir - download directory as zip

        rmfile - remove file
        upfile - upload file
        downfile - download file
    """
    op = request.GET['op']
    if op == 'ls':
        data = fsop.ls(request.GET['dirID'])
        return JsonResponse(data)
    elif op == 'mkdir':
        Directory.make()
    elif op == 'rmdir':
        Directory.remove()
    elif op == 'updir':
        Directory.upload()
    elif op == 'downdir':
        Directory.download()
    elif op == 'rmfile':
        File.remove()
    elif op == 'upfile':
        File.upload()
    elif op == 'downfile':
        File.download()
    else:
        pass
