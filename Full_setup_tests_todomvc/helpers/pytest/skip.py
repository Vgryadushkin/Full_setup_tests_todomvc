import pytest


def pending(test_fn):
    def decorated(*args, **kwargs):
        test_fn(*args, **kwargs)
        pytest.skip('as pending')
    return decorated
