import pytest

from core.config import (
    AwsSecretsManagerProvider,
    EnvSecretsProvider,
    SecretNotFoundError,
    Settings,
    get_secrets_provider,
)


class FakeClient:
    def __init__(self, secrets: dict[str, str]) -> None:
        self.secrets = secrets
        self.calls: list[str] = []

    def get_secret_value(self, SecretId: str) -> dict[str, str]:  # noqa: N803
        self.calls.append(SecretId)
        if SecretId not in self.secrets:
            raise KeyError(SecretId)
        return {"SecretString": self.secrets[SecretId]}


def test_env_provider_reads_and_fails_closed() -> None:
    provider = EnvSecretsProvider({"A": "x"})
    assert provider.get_secret("A") == "x"
    with pytest.raises(SecretNotFoundError):
        provider.get_secret("MISSING")


def test_aws_provider_uses_injected_client() -> None:
    client = FakeClient({"db": "pw"})
    provider = AwsSecretsManagerProvider(client=client)
    assert provider.get_secret("db") == "pw"
    assert client.calls == ["db"]
    with pytest.raises(SecretNotFoundError):
        provider.get_secret("nope")


def test_platform_phase_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PLATFORM_PHASE", "3")
    assert Settings(_env_file=None).platform_phase == 3  # type: ignore[call-arg]


def test_provider_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PLATFORM_PHASE", raising=False)
    local = Settings(_env_file=None, environment="local")  # type: ignore[call-arg]
    assert isinstance(get_secrets_provider(local), EnvSecretsProvider)
    prod = Settings(_env_file=None, environment="prod")  # type: ignore[call-arg]
    assert isinstance(get_secrets_provider(prod), AwsSecretsManagerProvider)
