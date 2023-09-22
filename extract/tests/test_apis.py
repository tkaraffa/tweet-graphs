import pytest

from src.apis import APIs, get_api_class


@pytest.mark.parametrize(
    "api, expected_exception",
    [
        *[(api.name, None) for api in APIs],
        ("DNE", ValueError),
        ("Does not exist", ValueError),
    ],
)
def test_get_api_class(api: str, expected_exception: Exception):
    if expected_exception is None:
        assert get_api_class(api) is not None
    else:
        with pytest.raises(expected_exception):
            get_api_class(api)
