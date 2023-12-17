from pathlib import Path
import logging
import shutil
import re
import typing

import pydantic

Mapper: typing.TypeAlias = typing.Callable[[Path, Path], Path]


class Incoming2NativeMap(pydantic.BaseModel):
    src_pattern: re.Pattern
    repl: str
    mapper: Mapper

    def map(self, file: Path, outroot: Path) -> Path:
        # double-check mapping makes sense
        matches = self.src_pattern.search(str(file))
        if not matches:
            msg = f"{file=} does not match this object's src_pattern {self.src_pattern}"
            raise ValueError(msg)

        to_create = self.src_pattern.sub(self.repl, matches.group(0))

        return self.mapper(file, outroot / to_create)

    @classmethod
    def from_str(
        cls, src_pattern: str, repl: str, mapper: Mapper
    ) -> "Incoming2NativeMap":
        return cls(
            src_pattern=re.compile(src_pattern),
            repl=repl,
            mapper=mapper,
        )


def unpack_archive(src: Path, dst: Path) -> Path:
    logging.info(f"extracting {src} -> {dst}")
    shutil.unpack_archive(src, extract_dir=dst)
    src.unlink()
    return dst


def move(src: Path, dst: Path) -> Path:
    logging.info(f"moving {src} -> {dst}")
    if not (parent := dst.parent).exists():
        parent.mkdir(parents=True)

    shutil.move(src, dst)

    return dst
