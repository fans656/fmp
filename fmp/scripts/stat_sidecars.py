import argparse

from fans.path import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    args = parser.parse_args()

    tag_to_info = {}

    root_dir = Path(args.root)
    for sidecar_path in root_dir.iterdir():
        name = sidecar_path.name
        tags_path = sidecar_path / 'tags.json'
        if tags_path.exists():
            tags = Path(tags_path).load().get('tags', [])
            for tag in tags:
                values = tag.get('tag', '').split()
                for value in values:
                    if value not in tag_to_info:
                        tag_to_info[value] = {
                            'count': 0,
                        }
                    info = tag_to_info[value]
                    info['count'] += 1

    for tag, info in sorted(
            tag_to_info.items(),
            key=lambda d: d[1]['count'],
            reverse=True,
    ):
        count = info['count']
        print(f'{count:2} {tag}')
