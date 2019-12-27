from .models import Directory, File


def ls(dirID):
    def dir_to_dict(id):
        d = Directory.objects.get(pk=id)
        children = [dir_to_dict(sd.pk) for sd in Directory.subdirs(d)]
        children += [file_to_dict(f.pk) for f in Directory.files(d)]
        return {
            'id': d.pk,
            'name': d.name,
            'type': 'dir',
            'children': children,
        }

    def file_to_dict(id):
        f = File.objects.get(pk=id)
        return {
            'id': f.pk,
            'name': f.name,
            'type': 'file',
        }

    def make_paths(d, path):
        for c in d['children']:
            c['path'] = path
            if c['type'] == 'dir':
                make_paths(c, path + [d['id']])

    d = dir_to_dict(dirID)
    d['path'] = []
    make_paths(d, [d['id']])
    return d
