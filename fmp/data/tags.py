from fans.path import make_paths, Path

from fmp.logic.utils import find_nearest


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
    def template_tags(self):
        return list({d['tag']: d for d in self.tags if d.get('tag')}.values())

    @property
    def sorted_tags(self):
        return sorted(self.tags, key=lambda d: d['time_pos'])

    @property
    def reversed_tags(self):
        return sorted(self.tags, key=lambda d: d['time_pos'], reverse=True)

    def load(self):
        return self.fpath.load(default={'tags': []})

    def save(self, data):
        self.fpath.save(data, indent=2, ensure_ascii=False)

    def find_nearest_tag(self, time_pos):
        return find_nearest(self.sorted_tags, time_pos, key='time_pos')

    def find_prev_tag(self, time_pos):
        tag = self.find_nearest_tag(time_pos)
        if tag:
            if tag['time_pos'] < time_pos:
                return tag
            else:
                return self.get_prev_tag(tag)

    def find_next_tag(self, time_pos):
        tag = self.find_nearest_tag(time_pos)
        if tag:
            if time_pos < tag['time_pos']:
                return tag
            else:
                return self.get_next_tag(tag)

    def get_prev_tag(self, target):
        tags = self.sorted_tags
        for i, tag in enumerate(tags):
            if tag['time_pos'] == target['time_pos']:
                return tags[i - 1] if i - 1 >= 0 else tags[-1]

    def get_next_tag(self, target):
        tags = self.sorted_tags
        for i, tag in enumerate(tags):
            if tag['time_pos'] == target['time_pos']:
                return tags[i + 1] if i + 1 < len(tags) else tags[0]
