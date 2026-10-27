# bestcf-IP

每天北京时间 08:00 自动合并 6 个地区（TW / HK / SG / JP / NL / US）的 BestCF 优选 IP 文件。

## 怎么填地址（不用改程序）

每个地区一个地址文件，放在 `sources/` 里，每行一个待合并文件的 URL，`#` 开头是注释：

- `sources/tw.txt`：TW，已填好 3 个地址
- `sources/hk.txt`：HK，待填
- `sources/sg.txt`：SG，待填
- `sources/jp.txt`：JP，待填
- `sources/nl.txt`：NL，待填
- `sources/us.txt`：US，待填

在 GitHub 网页上直接点开 `sources/hk.txt` 等文件 → 编辑 → 每行粘贴一个地址 → 保存即可。下一次定时（或手动 Run workflow）就会生成对应输出。

## 输出（仓库根目录，每个地区一个）

```
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/tw.txt
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/hk.txt
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/sg.txt
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/jp.txt
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/nl.txt
https://raw.githubusercontent.com/duduskying/bestcf-IP/main/us.txt
```

地址文件还是空的地区会被跳过，不会把旧输出清空；等你填好地址后才开始生成该地区的文件。

## 合并规则

- 按地址文件里的顺序拉取，同一地区内按 `#` 前的 IP:端口去重，首次出现为准。
- BestCF 风格文件的首尾标题/推广行不算节点（IP 为 162.159.198.1 / 162.159.197.1 且备注含“版”或“分享”时跳过），合并文件只保留一条合并标题和一条推广尾行。
- 节点之间空一行；标题里不带日期，避免日期变化导致每天无意义提交，更新时间以提交时间为准。
- 某地址拉取失败时警告并继续用该地区其他地址；某地区最终 0 条时跳过该地区，不覆盖旧输出。
- 内容不变时不提交。

## 手动触发

仓库 Actions 页 → merge-bestcf → Run workflow。
