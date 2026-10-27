# bestcf-tw-merged

每天北京时间 08:00 自动合并 3 个 BestCF TW 优选 IP 文件，输出 `tw.txt`。

来源（按此顺序，先出现为准）：
- https://bestcf.pages.dev/s5gy/tw.txt
- https://bestcf.pages.dev/tiancheng/tw.txt
- https://bestcf.pages.dev/tiancheng2/tw.txt

合并规则：按 `#` 前的 IP:端口去重，重复的整行丢弃；各源首尾的标题/推广行不算节点，合并文件只保留一条合并标题和一条推广尾行。内容不变时不提交。

使用（合并后文件直链，仓库建好后生效）：
```
https://raw.githubusercontent.com/duduskying/bestcf-tw-merged/main/tw.txt
```

手动触发：仓库 Actions 页 → merge-bestcf-tw → Run workflow。
