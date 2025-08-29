import math
from turtledemo.minimal_hanoi import hanoi

import pytest, os
import logging


# @pytest.fixture(scope="function")  # default
# @pytest.fixture(scope="class")
# @pytest.fixture(scope="module")
# @pytest.fixture(scope="package")   # pytest>=8
# @pytest.fixture(scope="session")
# function: fresh per test (most common).
# session: created once per test run (great for expensive resources like DB containers).


def test_numbers_and_types():
    x = 5
    assert x == 5                  # equality
    assert isinstance(x, int)      # type
    assert x in {3, 4, 5}          # membership
    assert 1 < x <= 5              # chained comparisons

def test_strings_and_substrings():
    s = "hello pytest"
    assert s.startswith("hello")
    assert "py" in s               # substring
    assert s.endswith("test")

def test_lists_and_sets():
    xs = [1, 2, 3]
    assert xs == [1, 2, 3]         # order matters
    assert set(xs) == {3, 2, 1}    # order independent

def test_dicts_diff_nicely():
    user = {"id": 1, "name": "Lakshay", "role": "tester"}
    expected = {"id": 1, "name": "Lakshay", "role": "tester"}
    assert user == expected        # pytest shows key-by-key diffs if it fails


# custom message
def test_with_message():
    count = 4
    assert count >= 4, "should have loaded at at least 4 times"


#approx
def test_float_comparison():
    assert (0.1 + 0.2) == pytest.approx(0.3, rel=1e-12)
    assert math.sqrt(2) == pytest.approx(1.41421356237, abs=.2)

@pytest.fixture()
def sample_user():
    return {"id" : 1, "name": "Lakshay"}

def test_uses_fixture(sample_user):
    assert sample_user["name"] == "Lakshay"

# teardown with yield

# def opened_file(tmp_path):
#     f = tmp_path / "data.txt"
#     f.write_text("hello")
#     #setup
#     handle = f.open()
#     try:
#         yield handle
#     finally:
#         handle.close()


# tests/test_api_client.py
def test_base(api_base_url):
    assert api_base_url.endswith("/api")

# tmp_path → fresh pathlib.Path per test.
def test_tmp_path_roundtrip(tmp_path):
    p = tmp_path / "notes.txt"
    p.write_text("pytest is neat")
    assert p.read_text() == "pytest is neat"

# tmp_path_factory → create named bases across tests / larger scope.
def test_shared_area(tmp_path_factory):
    base = tmp_path_factory.mktemp("workspace")
    f = base / "log.txt"
    f.write_text("hello")
    assert f.exists()

def greet():
    import os
    return f"Hi {os.getenv('USER', 'anon')}"

def test_env(monkeypatch):
    monkeypatch.setenv("USER", "Lakshay")
    assert greet() == "Hi Lakshay"

def test_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    # code under test that writes files will now use tmp_path as cwd



# capture stdout/stderr & logs: capsys, capfd, caplog
def cli():
    print("OK")
    raise SystemExit(0)

def test_cli_output_and_exit(capsys):
    try:
        cli()
    except SystemExit as e:
        assert e.code == 0
    out, err = capsys.readouterr()
    assert "OK" in out

logger = logging.getLogger("app")

def do_work():
    logger.info("started")
    logger.warning("low disk")

def test_logs(caplog):
    with caplog.at_level(logging.INFO, logger="app"):
        do_work()
    assert ("app", logging.WARNING, "low disk") in  caplog.record_tuples

def test_user_factory(user_factory):
    u1 = user_factory()
    u2 = user_factory(id=2, role="sdet")
    assert u1["name"] == "Lakshay" and u2["role"] == "sdet"

# Fixtures can depend on other fixtures via parameters.

def test_client(client):
    assert client.tok == "secret-token"

# monkeypatch — safe, temporary patching inside tests

def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-123")
    monkeypatch.delenv("Home", raising=False)

# def test_sttrs(monkeypatch):
#     import time
#     monkeypatch.setattr(time, "time", lambda: 123.456)
#     monkeypatch.setattr("pathlib.path.home", lambda: "/fake/home", raising= False)

def test_items(monkeypatch):
    cfg = {"retries": 3}
    monkeypatch.setitem(cfg, "retries", 10)
    monkeypatch.delitem(cfg, "retries", raising=False)

def test_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

# Keep patches local to a test when possible; if many tests need the same patch, wrap it in a fixture.

import os, sys

def write_low_level():
    os.write(1, b"STDOUT via os.write\n")
    os.write(2, b"STDERR via os.write\n")

def test_low_level(capfd):
    write_low_level()
    out, err = capfd.readouterr()
    assert "STDOUT via os.write" in out
    assert "STDERR via os.write" in err

def greet_cli(name: str) -> None:
    print(f"Hello, {name}!")
    print("Oops", file=sys.stderr)

def test_greet_cli(capsys):
    greet_cli("Lakshay")
    out, err = capsys.readouterr()     # flush & read
    assert "Hello, Lakshay!" in out
    assert "Oops" in err

