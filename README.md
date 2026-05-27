# DacDpkLocalizer

DPK/DACZ 本地化工具。支持 DPK 解包/回封、脚本加密层自动探测、分文件 DSAT 双行文本导出、导入回封、零编辑校验和加长回封。

`生成IR` 时会读取 `profiles/*.json`，对 DPK 内候选脚本逐个尝试已知加密 profile，按解码结果评分，成功后在 IR 中记录 `crypto_profile`、动态派生的 `key` 和 `probe_score`。回封时按记录的 profile 与新文件大小重新派生 key。

## GUI

```bash
python run_gui.py
```

常用操作：

- 素材包：`解包DPK` → 编辑 `workspace/unpack/` → `回封解包目录`
- 脚本包：`生成IR` → `导出文本` → 编辑 `texts/by_source/*.dsat.txt` → `导入文本并回封` → `验证`

## CLI

```bash
python run_cli.py unpack-dpk input.dpk -o workspace/unpack
python run_cli.py repack-dpk workspace/unpack -o rebuilt.dpk

python run_cli.py disasm script.dpk -o script_workspace --encoding cp932
python run_cli.py export-asm script_workspace
python run_cli.py export-text script_workspace -o script_workspace
python run_cli.py import-text script_workspace script_workspace/texts/by_source -o script_workspace/rebuilt/script_patched.dpk --allow-lengthen
python run_cli.py verify script.dpk script_workspace/rebuilt/script_patched.dpk -o script_workspace/reports
python run_cli.py smoke-roundtrip script.dpk -o smoke_test --encoding cp932
```

## Profile 扩展

内置 profile 在：

```text
profiles/dacz_filename_size_lcg.json
```

如果另一个同引擎游戏使用同一算法，直接放 DPK 即可自动探测。若新游戏变体常量或扩展名不同，不改主程序，新建一个 `profiles/xxx.json` 即可。未知算法无法只靠 DPK 凭空推出，需要先通过 EXE 静态分析补一个 profile，然后再让工具自动探测。

## 文本目录

只编辑：

```text
texts/by_source/*.dsat.txt
```

只改 `●` 行，保留索引、tag 和 `{{XX}}` / `{{XX:YY}}` 这类占位符。
