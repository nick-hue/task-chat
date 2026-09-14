import pytest

from parser import parse


@pytest.mark.parametrize(
    "text, folder, content, tags",
    [
        ("buy milk", "inbox", "buy milk", []),
        ("@work buy milk", "work", "buy milk", []),
        ("@work buy milk #urgent", "work", "buy milk", ["urgent"]),
        ("email bob@example.com", "inbox", "email bob@example.com", []),
        ("@work email bob@example.com", "work", "email bob@example.com", []),
        (
            "@work email bob@example.com #check #test",
            "work",
            "email bob@example.com",
            ["check", "test"],
        ),
        ("buy #urgent milk", "inbox", "buy milk", ["urgent"]),
        ("@work @home buy milk", "work", "@home buy milk", []),
        ("milk #Urgent #urgent", "inbox", "milk", ["urgent"]),
        ("milk #urgent.", "inbox", "milk .", ["urgent"]),
        ("issue #42", "inbox", "issue", ["42"]),
    ],
)
def test_parse(text, folder, content, tags):
    result = parse(text)
    assert result.folder == folder
    assert result.content == content
    assert result.tags == tags


@pytest.mark.parametrize("text", ["@work #urgent", "   "])
def test_parse_rejects_empty_content(text):
    with pytest.raises(ValueError):
        parse(text)
