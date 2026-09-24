from api.cricbuzz_client import CricbuzzClient, CricbuzzAPIError


def test_client_reports_not_configured_without_key(monkeypatch):
    from utils import config as config_module
    monkeypatch.setattr(config_module.settings, "cricbuzz_api_key", "")
    client = CricbuzzClient()
    assert client.is_configured() is False


def test_request_raises_when_not_configured(monkeypatch):
    from utils import config as config_module
    monkeypatch.setattr(config_module.settings, "cricbuzz_api_key", "")
    client = CricbuzzClient()
    try:
        client._request("/matches/v1/live")
        assert False, "Expected CricbuzzAPIError"
    except CricbuzzAPIError:
        pass
