from fans.path import make_paths, Path


class Tags:

    def __init__(self, dir_path: Path):
        self.fpath = dir_path / 'tags.json'

    def add(self, tag: dict):
        data = self.load()
        data['tags'].append(tag)
        self.save(data)

    def delete(self, tag):
        data = self.load()
        data['tags'] = [d for d in data['tags'] if d['time_pos'] != tag['time_pos']]
        self.save(data)

    def update(self, tag):
        # NOTE: tag dict already updated by caller
        data = self.load()
        data['tags'] = [tag if d['time_pos'] == tag['time_pos'] else d for d in data['tags']]
        self.save(data)

    @property
    def tags(self):
        return self.load()['tags']

    def load(self):
        return self.fpath.load(default={'tags': []})

    def save(self, data):
        self.fpath.save(data, indent=2, ensure_ascii=False)

