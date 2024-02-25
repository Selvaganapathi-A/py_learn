import os
import zipfile
from pathlib import Path


def main():
    pathlike: Path = Path("./notebooks/")
    if not (pathlike.exists() or pathlike.is_dir()):
        return None
    with zipfile.ZipFile(
        file=pathlike.parent / (pathlike.name + "-compressed.zip"),
        mode="w",
        compresslevel=2,
        compression=zipfile.ZIP_LZMA,
    ) as writer:
        for root, _, files in os.walk(pathlike):
            root_dir: Path = Path(root)
            for file in files:
                filepath: Path = root_dir / file
                rel_path: Path = filepath.relative_to(pathlike)
                writer.write(
                    filepath,
                    rel_path,
                    compresslevel=zipfile.ZIP_BZIP2,
                )
                print(filepath)
                print(rel_path)
        writer.close()
    print("Task Completed.")


if __name__ == "__main__":
    main()
    pass
