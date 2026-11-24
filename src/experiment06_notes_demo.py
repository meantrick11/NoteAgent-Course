"""独立演示笔记仓库模块的创建、写入和读取接口。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from noteagent.notes.repository import FileNoteRepository, NotePathError


def main() -> None:
    """在临时目录中调用笔记仓库，不改动项目的正式笔记。"""
    with TemporaryDirectory() as temporary_dir:
        notes = FileNoteRepository(Path(temporary_dir))
        file_name = notes.create("Experiment6.md", "实验6")
        print(f"创建笔记：{file_name}")

        notes.write(file_name, "## 模块调用\n笔记写入成功。\n")
        print("追加后读取：")
        print(notes.read(file_name), end="")
        print(f"笔记列表：{', '.join(notes.list_notes())}")

        notes.write(file_name, "# 实验6（已覆盖）\n", append=False)
        print("覆盖后读取：")
        print(notes.read(file_name), end="")

        try:
            notes.read("../outside.md")
        except NotePathError:
            print("路径校验：已拒绝访问笔记目录之外的文件")


if __name__ == "__main__":
    main()
