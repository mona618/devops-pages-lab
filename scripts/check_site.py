"""Small content gate for the GitHub Pages assignment."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!--START_SECTION:activity-->"
END = "<!--END_SECTION:activity-->"


class BasicPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = False
        self.viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self.title = True
        if tag == "meta" and attributes.get("name") == "viewport":
            self.viewport = True


def main() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "index.md").read_text(encoding="utf-8")
    layout = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
    basic = (ROOT / "docs/index.html").read_text(encoding="utf-8")

    assert readme.count(START) == 1 and readme.count(END) == 1, "Activity markers must appear once each"
    assert readme.index(START) < readme.index(END), "Activity markers are reversed"
    assert "{% include_relative README.md %}" in index, "Homepage must include README"
    assert "layout: default" in index, "Homepage must use the custom layout"
    assert "{{ content }}" in layout, "Layout must render page content"
    assert (ROOT / "assets/site.css").is_file(), "Custom stylesheet is missing"

    parser = BasicPageParser()
    parser.feed(basic)
    assert parser.title and parser.viewport, "Basic HTML page needs title and viewport"
    assert "mona618" in basic and "DevOps" in basic, "Basic HTML page needs owner and course"
    print("PASS: activity markers, README homepage, custom layout, stylesheet, and basic HTML page")


if __name__ == "__main__":
    main()

