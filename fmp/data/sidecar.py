import contextlib

from fans.path import make_paths, Path

from fmp.data.tags import Tags


class Sidecar:

    def __init__(self, fpath: str, conf: dict):
        self.conf = conf
        if conf.get('sidecar'):
            self.dir_path = Path(conf['sidecar']) / f'{Path(fpath).name}.sidecar'
        else:
            self.dir_path = Path(f'{fpath}.sidecar')

    @property
    def tags(self):
        @contextlib.contextmanager
        def _tags():
            self.dir_path.ensure_dir()
            yield Tags(self.dir_path, conf=self.conf)
        return _tags()
