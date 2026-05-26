# DacDpkLocalizer

DPK/DACZ 本地化工具。支持 DPK 解包、回封，脚本解密、分文件双行文本导出、导入回封、零编辑校验和加长回封。

## GUI

```bash
python run_gui.py
```

Windows 可双击：

```text
启动GUI.bat
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
```

## 文本目录

只编辑：

```text
texts/by_source/*.dsat.txt
```

只改 `●` 行，保留索引、tag 和 `{{XX}}` / `{{XX:YY}}` 这类占位符。
