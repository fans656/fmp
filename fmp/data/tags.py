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

    @property
    def reversed_tags(self):
        return sorted(self.tags, key=lambda d: d['time_pos'], reverse=True)

    def load(self):
        return self.fpath.load(default={'tags': []})

    def save(self, data):
        self.fpath.save(data, indent=2, ensure_ascii=False)

    def find_nearest_tag(self, time_pos):
        ret = None
        min_dis = float('inf')
        for tag in self.reversed_tags:
            dis = abs(tag['time_pos'] - time_pos)
            if dis < min_dis or dis == min_dis and tag['time_pos'] < time_pos:
                min_dis = dis
                ret = tag
        return ret
