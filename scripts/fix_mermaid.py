from pathlib import Path
import re

article = Path("src/content/articles/cloud-infrastructure.md")
text = article.read_text(encoding="utf-8")

# Select the Mermaid block in the architecture section (approximately lines 358-425).
blocks = list(re.finditer(r"```mermaid\r?\n.*?\r?\n```", text, flags=re.DOTALL))
if not blocks:
    raise RuntimeError("No Mermaid diagram found")
block_match = next((m for m in blocks if 300 <= text.count("\n", 0, m.start()) + 1 <= 450), None)
if block_match is None:
    raise RuntimeError("No Mermaid diagram found near lines 358-425")

emoji = re.compile(
    r"[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE0E\U0000FE0F\U0000200D\U0001F3FB-\U0001F3FF]"
)
old_block = block_match.group(0)
lines = old_block.splitlines(keepends=True)
cleaned_lines = []
for line in lines:
    if line.startswith("```"):
        cleaned_lines.append(line)
        continue
    line = emoji.sub("", line)
    # Remove whitespace left at the edges of bracketed node labels.
    line = re.sub(r"\[\s+", "[", line)
    line = re.sub(r"\s+\]", "]", line)
    cleaned_lines.append(line)
new_block = "".join(cleaned_lines)
text = text[:block_match.start()] + new_block + text[block_match.end():]

# Write an explicit UTF-8 BOM while retaining UTF-8 text for future emoji additions.
article.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))

# Verification: BOM, valid UTF-8, one target diagram, and no emoji in it.
raw = article.read_bytes()
if not raw.startswith(b"\xef\xbb\xbf"):
    raise RuntimeError("UTF-8 BOM was not written")
written = raw[3:].decode("utf-8")
verified = next((m.group(0) for m in re.finditer(r"```mermaid\r?\n.*?\r?\n```", written, flags=re.DOTALL)
                 if 300 <= written.count("\n", 0, m.start()) + 1 <= 450), None)
if verified is None or emoji.search(verified):
    raise RuntimeError("Diagram verification failed")
print(f"Updated {article} ({len(verified.splitlines())} Mermaid lines); UTF-8 BOM verified; emojis removed.")
