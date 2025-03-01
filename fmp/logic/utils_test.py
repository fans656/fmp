from .utils import find_nearest


def test_find_nearest():
    tags = [
        {'time_pos': 0.0},
        {'time_pos': 1.0},
    ]

    assert find_nearest(tags, 0.0, key='time_pos')['time_pos'] == 0.0
    assert find_nearest(tags, 0.1, key='time_pos')['time_pos'] == 0.0
    assert find_nearest(tags, 0.4, key='time_pos')['time_pos'] == 0.0
    assert find_nearest(tags, 0.5, key='time_pos')['time_pos'] == 0.0

    assert find_nearest(tags, 0.6, key='time_pos')['time_pos'] == 1.0
    assert find_nearest(tags, 0.8, key='time_pos')['time_pos'] == 1.0
    assert find_nearest(tags, 1.0, key='time_pos')['time_pos'] == 1.0

    assert find_nearest(tags, -1.0, key='time_pos')['time_pos'] == 0.0
    assert find_nearest(tags, 2.0, key='time_pos')['time_pos'] == 1.0
