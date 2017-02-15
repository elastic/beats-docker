def test_base_os(SystemInfo):
    assert SystemInfo.distribution == 'ubuntu'
    assert SystemInfo.release == '16.04'
