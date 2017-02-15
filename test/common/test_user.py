import os

beat = os.environ['BEAT']


def test_group(Group):
    group = Group(beat)
    assert group.exists
    assert group.gid == 1000


def test_user(User):
    user = User(beat)
    assert user.uid == 1000
    assert user.gid == 1000
    assert user.group == beat
    assert user.home == '/usr/share/%s' % beat
    assert user.shell == '/bin/bash'
