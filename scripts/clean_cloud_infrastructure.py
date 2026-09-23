from pathlib import Path
import re

ARTICLE_PATH = Path(r"C:\personal\voidstack-complete\voidstack\src\content\articles\cloud-infrastructure.md")


def main() -> None:
    raw = ARTICLE_PATH.read_text(encoding="utf-8")
    raw = raw.replace("\ufeff", "")

    # Remove every YAML-style frontmatter block delimited by lines containing only ---.
    without_frontmatter = re.sub(
        r"(?ms)^---[ \t]*\r?\n.*?^---[ \t]*(?:\r?\n|$)",
        "",
        raw,
    )

    heading = "# Understanding Cloud Infrastructure"
    heading_match = re.search(r"(?m)^# Understanding Cloud Infrastructure[ \t]*$", without_frontmatter)
    if heading_match is None:
        raise ValueError(f"Could not find article heading: {heading}")

    article = without_frontmatter[heading_match.start():].strip()
    frontmatter = """---
title: 'Understanding Cloud Infrastructure'
description: 'A beginner-friendly guide to compute, networking, storage, and managed services with practical examples.'
category: 'CLOUD'
publishedDate: 2026-09-21
---"""
    clean_content = frontmatter + "\n\n" + article + "\n"

    # Python's utf-8 codec writes no BOM.
    ARTICLE_PATH.write_text(clean_content, encoding="utf-8", newline="\n")

    # Verify the resulting file and its encoding/content shape.
    written_bytes = ARTICLE_PATH.read_bytes()
    if written_bytes.startswith(b"\xef\xbb\xbf"):
        raise AssertionError("Output contains a UTF-8 BOM")
    written = written_bytes.decode("utf-8")
    expected_prefix = frontmatter + "\n\n" + heading
    if not written.startswith(expected_prefix):
        raise AssertionError("Output does not start with the expected frontmatter and article heading")
    if written.count("publishedDate: 2026-09-21") != 1:
        raise AssertionError("publishedDate is missing or duplicated")
    if re.search(r"(?m)^publishedDate:\s*['\"]", written):
        raise AssertionError("publishedDate is quoted")
    if written[written.index("---", 4) + 3:].lstrip("\r\n").startswith("---"):
        raise AssertionError("Unexpected second frontmatter delimiter")

    print(f"Verified: {ARTICLE_PATH}")
    print(f"Bytes: {len(written_bytes)}; BOM: absent; Article heading: present")


if __name__ == "__main__":
    main()
