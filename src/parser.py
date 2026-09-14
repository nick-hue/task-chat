from dataclasses import dataclass, field
import re


@dataclass
class Result:
    content: str
    folder: str
    tags: list[str] = field(default_factory=list)


TAG_RE = re.compile(r"#([\w-]+)")


def parse(text: str) -> Result:

    data = text.split()

    folder = None

    if data and data[0].startswith("@") and len(data[0]) > 1:
        folder = data[0][1:]
        rest = data[1:]
    else:
        folder = "inbox"
        rest = data

    final_text = " ".join(rest)
    tags = list(dict.fromkeys(t.lower() for t in TAG_RE.findall(final_text)))

    content = " ".join(TAG_RE.sub("", final_text).split())
    if not content:
        raise ValueError("no task text found")
    res = Result(content=content, folder=folder, tags=tags)
    return res


if __name__ == "__main__":
    parse("@work buy milk #test1 #test2 #TEST3 #TEST3 #urgent #Urgent")
