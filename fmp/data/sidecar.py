import contextlib

from fans.path import make_paths, Path

from fmp.data.tags import Tags


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
