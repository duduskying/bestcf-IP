#!/usr/bin/env python3
"""合并 3 个 BestCF TW 优选 IP 文件，去重后输出一个文件。

规则（与本次手工预览一致）：
- 按用户给的顺序拉取：s5gy -> tiancheng -> tiancheng2
- 去重键 = # 前的 IP:端口，首次出现为准，后面重复的整行丢弃
- 162.159.198.1 / 162.159.197.1 两行是各源的首尾标题/推广行，不算节点，
  合并文件只保留一条合并标题和一条推广尾行
- 空行格式照原文件：节点之间空一行
"""
import sys
import urllib.request

SOURCES = [
    "https://bestcf.pages.dev/s5gy/tw.txt",
    "https://bestcf.pages.dev/tiancheng/tw.txt",
    "https://bestcf.pages.dev/tiancheng2/tw.txt",
]

HEADER_IP = "162.159.198.1:443"
FOOTER_IP = "162.159.197.1:443"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bestcf-merge/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def main(out_path):
    seen = set()
    entries = []
    for url in SOURCES:
        for line in fetch(url).splitlines():
            line = line.strip()
            if not line or "#" not in line:
                continue
            key = line.split("#", 1)[0].strip()
            if key in (HEADER_IP, FOOTER_IP) or key in seen:
                continue
            seen.add(key)
            entries.append(line)
    header = f"{HEADER_IP}#合并 TW版 | BestCF.pages.dev"
    footer = f"{FOOTER_IP}#合并 | 分享免费优选网 BestCF.pages.dev"
    body = "\n\n".join(entries)
    text = f"{header}\n\n{body}\n\n{footer}\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"merged {len(entries)} unique entries from {len(SOURCES)} sources -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tw.txt")
