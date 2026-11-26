"""Unit tests for local integration adapters (R3.4)."""

from __future__ import annotations

import json
import logging
import shutil
import tempfile
from pathlib import Path

import pytest

from core.integrations import (
    AuthUnavailableError,
    EmailMessage,
    FilesystemStorage,
    LocalDevAuthProvider,
    ModelInvocationError,
    OutboxEmailSender,
    RecordedModelClient,
    StorageError,
    StubMalwareScanner,
    SubstitutionRegistry,
    register_local,
)


@pytest.fixture
def workdir():
    path = Path(tempfile.mkdtemp())
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@pytest.mark.parametrize(
    "data,name",
    [(b"", "a.txt"), (b"hello", "b.pdf"), (b"X5O!P%@AP", "eicar.com")],
)
def test_stub_scanner_never_reports_clean(data, name):
    result = StubMalwareScanner().scan(data, name)
    assert result.status == "unavailable"
    assert result.status != "clean"


@pytest.mark.parametrize("env", ["production", "staging", "dev", "Local", ""])
def test_local_auth_refuses_outside_local(env):
    with pytest.raises(AuthUnavailableError):
        LocalDevAuthProvider(env)


def test_local_auth_round_trip_in_local():
    auth = LocalDevAuthProvider("local", signing_key="k")
    identity = auth.verify_token(auth.issue_token("u1", ("admin",)))
    assert identity.subject == "u1"
    assert identity.roles == ("admin",)


def test_local_auth_rejects_tampered_token():
    auth = LocalDevAuthProvider("local", signing_key="k")
    other = LocalDevAuthProvider("local", signing_key="other")
    with pytest.raises(ValueError):
        auth.verify_token(other.issue_token("u1"))
    with pytest.raises(ValueError):
        auth.verify_token("garbage")


def test_outbox_records_locally_and_never_claims_delivery(workdir, caplog):
    outbox = workdir / "out" / "outbox.jsonl"
    sender = OutboxEmailSender(outbox)
    msg = EmailMessage(to="a@example.com", subject="Hi", body="Body")
    with caplog.at_level(logging.INFO, logger="core.integrations.local"):
        assert sender.send(msg) is None  # no delivery receipt/result
    lines = outbox.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["to"] == "a@example.com"
    text = " ".join(r.getMessage().lower() for r in caplog.records)
    assert "outbox" in text
    assert "delivered" not in text
    assert "sent" not in text


def test_storage_round_trip_and_delete(workdir):
    store = FilesystemStorage(workdir)
    store.put("a/b.txt", b"data")
    assert store.get("a/b.txt") == b"data"
    store.delete("a/b.txt")
    with pytest.raises(StorageError):
        store.get("a/b.txt")


@pytest.mark.parametrize("key", ["../escape.txt", "a/../../escape.txt", "", "."])
def test_storage_rejects_keys_escaping_root(workdir, key):
    root = workdir / "root"
    root.mkdir()
    store = FilesystemStorage(root)
    with pytest.raises(StorageError):
        store.put(key, b"x")
    assert not (workdir / "escape.txt").exists()


def test_recorded_model_client():
    client = RecordedModelClient({"p": "out"})
    assert client.invoke("p") == "out"
    with pytest.raises(ModelInvocationError):
        client.invoke("unrecorded")


def test_registry_lists_active_substitutions():
    registry = SubstitutionRegistry()
    assert registry.list_active() == []
    register_local(registry, "MalwareScanner")
    register_local(registry, "EmailSender")
    active = registry.list_active()
    assert [s.interface for s in active] == ["EmailSender", "MalwareScanner"]
    assert active[1].local_adapter == "StubMalwareScanner"
    registry.unregister("EmailSender")
    assert [s.interface for s in registry.list_active()] == ["MalwareScanner"]
    assert registry.as_records()[0]["interface"] == "MalwareScanner"
