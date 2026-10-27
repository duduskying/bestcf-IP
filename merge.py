#!/usr/bin/env python3
"""多地区 BestCF 优选 IP 合并。

框架用法（用户只需填地址，不用改程序）：
- 每个地区一个地址文件，放在脚本同目录的 sources/ 里：
    sources/tw.txt  sources/hk.txt  sources/sg.txt
    sources/jp.txt  sources/nl.txt  sources/us.txt
- 地址文件里每行一个待合并文件的 URL，空行和 # 开头的注释行忽略。
  例如 sources/hk.txt：
    https://bestcf.pages.dev/xxx/hk.txt
    https://bestcf.pages.dev/yyy/hk.txt
- 输出在仓库根目录，每个地区一个文件：
    tw.txt  hk.txt  sg.txt  jp.txt  nl.txt  us.txt
  直链形如 https://raw.githubusercontent.com/duduskying/bestcf-IP/main/hk.txt
  （仓库改名后以新名为准）

合并规则（沿用 TW 首版）：
- 按地址文件里的顺序拉取，同一地区内按 IP:端口去重，首次出现为准。
- BestCF 风格文件的首尾标题/推广行不算节点：IP 是 162.159.198.1 或
  162.159.197.1，且备注里含“版”或“分享”时跳过；合并文件只保留一条
  合并标题和一条推广尾行。其他文件的同 IP 节点不受此影响。
- 节点之间空一行，与原文件格式一致；标题里不带日期，避免日期变化
  导致每天无意义提交，更新时间以提交时间为准。
- 容错：某地址拉取失败时警告并继续用该地区其他地址；某地区最终
  0 条时跳过该地区，不覆盖旧输出；全部地区都失败时返回非零。
"""
import sys
import urllib.request
from pathlib import Path

REGIONS = ["tw", "hk", "sg", "jp", "nl", "us"]
HEADER_IP = "162.159.198.1:443"
FOOTER_IP = "162.159.197.1:443"


def read_sources(sources_dir, region):
    path = sources_dir / f"{region}.txt"
    if not path.exists():
        return []
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bestcf-merge/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def merge_region(urls, region):
    seen = set()
    entries = []
    for url in urls:
        try:
            text = fetch(url)
        except Exception as e:  # noqa: BLE001 - 单个源失败不拖垮整个地区
            print(f"[{region}] warn: fetch failed {url}: {e}", file=sys.stderr)
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line or "#" not in line:
                continue
            key, remark = line.split("#", 1)
            key = key.strip()
            # 标题/推广行：只跳过备注含“版”或“分享”的那两行
            if key in (HEADER_IP, FOOTER_IP) and ("版" in remark or "分享" in remark):
                continue
            if key in seen:
                continue
            seen.add(key)
            entries.append(line)
    return entries


def main():
    base = Path(__file__).resolve().parent
    sources_dir = base / "sources"
    failed_regions = []
    wrote_regions = []
    for region in REGIONS:
        urls = read_sources(sources_dir, region)
        if not urls:
            print(f"[{region}] skip: no URLs in sources/{region}.txt")
            continue
        entries = merge_region(urls, region)
        if not entries:
            print(f"[{region}] skip: 0 entries, keep old output", file=sys.stderr)
            failed_regions.append(region)
            continue
        upper = region.upper()
        header = f"{HEADER_IP}#合并 {upper}版 | BestCF.pages.dev"
        footer = f"{FOOTER_IP}#合并 | 分享免费优选网 BestCF.pages.dev"
        text = f"{header}\n\n" + "\n\n".join(entries) + f"\n\n{footer}\n"
        (base / f"{region}.txt").write_text(text, encoding="utf-8")
        print(f"[{region}] merged {len(entries)} unique entries from {len(urls)} sources -> {region}.txt")
        wrote_regions.append(region)
    if wrote_regions and len(failed_regions) < len(REGIONS):
        return 0
    if not wrote_regions:
        print("error: no region produced output", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
