from .fixtures import beat


def test_group_properties(Group, beat):
    group = Group(beat.name)
    assert group.exists
    assert group.gid == 1000


def test_user_properties(User, beat):
    user = User(beat.name)
    assert user.uid == 1000
    assert user.gid == 1000
    assert user.group == beat.name
    assert user.home == '/usr/share/%s' % beat.name
    assert user.shell == '/bin/bash'
