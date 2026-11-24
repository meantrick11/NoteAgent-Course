# notes（代码包）

对数据目录（默认仓库根 `notes/`）做确定性 Markdown IO，并拦住路径逃逸。embedding 与 LLM 不在本包。Documents 的 HTTP 在 `router.py`，不经过 Agent。

## 包含模块

| 文件 | 模块 | 作用 |
|------|------|------|
| `repository.py` | `FileNoteRepository` | `list_notes` / `list_folders` / `create_folder` / `rename_folder` / `delete_folder` / `move` / `mtime` / `read` / `create` / `write` / `delete` / `exists` / `normalize` |
| `repository.py` | `NotePathError` | 空名、绝对路径、`..`、两层以上目录 |
| `router.py` | Documents HTTP | `GET/POST/PUT/DELETE /notes`、`POST /notes/{path}/index`、`POST /notes/folders`、`POST /notes/folders/rename`、`DELETE /notes/folders/{name}`、`POST /notes/move` |
| `schemas.py` | 请求/响应体 | 列表含 `mtime`、`indexed`（来自磁盘与 Chroma，无笔记表） |
| `__init__.py` | 再导出 | `from noteagent.notes import FileNoteRepository` |

## 基础使用

```python
from pathlib import Path
from noteagent.notes.repository import FileNoteRepository

repo = FileNoteRepository(Path("notes"))
repo.create("Go.md", "Go")           # 写入 "# Go\n\n"
repo.write("Go.md", "## 循环\n- 只有 for\n\n", append=True)
print(repo.read("Go.md"))
print(repo.list_notes())
print(repo.exists("Go.md"))
repo.delete("Go.md")
```

`write` 默认追加；`append=False` 为覆盖。文件必须已存在。相对路径可以是 `Go.md` 或一层 `Python/GIL.md`。`read("../x.md")` 与 `read("a/b/x.md")` 会抛 `NotePathError`。Documents 页面的 HTTP 契约见 [frontend.md](../../../docs/architecture/frontend.md) §5。

```bash
uv run pytest tests/unit/test_note_repository.py -q
```

## 实验 6：编码规范与模块化运行

本实验选取 `repository.py` 中的 `FileNoteRepository` 作为核心模块。它负责在指定目录内创建、写入、读取和列出 Markdown 笔记，并由 `NotePathError` 表示非法路径。Documents 路由 `router.py` 通过 `normalize`、`create` 等公开方法调用该模块；草稿审核逻辑也通过该模块写入正式笔记。

模块使用 `snake_case` 命名方法和变量，为公开方法标注参数与返回类型，并用文档字符串说明行为。文件读写统一指定 UTF-8；不存在、已存在和非法路径等情况抛出明确异常，由调用方处理。临时演示程序不会修改项目的 `notes/` 目录。

在仓库根目录独立运行演示程序：

```powershell
python src/experiment06_notes_demo.py
```

演示依次调用 `create`、`write`、`read`、`list_notes`，并检查覆盖写入与非法路径处理。程序使用 `TemporaryDirectory`，退出时自动清理演示文件。验证核心模块的现有单元测试：

```powershell
python -m pytest tests/unit/test_note_repository.py -q
```

本次验证结果为 `19 passed`。若所选 Python 环境没有安装 `pytest`，需要换用已安装该工具的环境运行测试；演示程序本身只依赖 Python 标准库和本仓库代码。
