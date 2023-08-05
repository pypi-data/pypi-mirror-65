from zo.aa import get_env, pp


def test_get_env():
    env = get_env('.env')
    # pp(env.dict())
    assert env.title == 'zo'
