import contextlib

from fans.path import make_paths, Path


class Sidecar:

    def __init__(self, fpath: str):
        self.dir_path = Path(f'{fpath}.sidecar')

    @property
    def tags(self):
        @contextlib.contextmanager
        def _tags():
            self.dir_path.ensure_dir()
            yield Tags(self.dir_path)
        return _tags()


class Tags:

    def __init__(self, dir_path: Path):
        self.fpath = dir_path / 'tags.json'

    def add(self, tag: dict):
        data = self.load()
        data['tags'].append(tag)
        self.fpath.save(data)

    def delete(self, tag):
        data = self.load()
        data['tags'] = [d for d in data['tags'] if d['time_pos'] != tag['time_pos']]
        self.fpath.save(data)

    @property
    def tags(self):
        return self.load()['tags']

    def load(self):
        return self.fpath.load(default={'tags': []})
