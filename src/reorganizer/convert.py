from pathlib import Path
import typing
import os

from reorganizer import mappers


def _attempt_map(
    src: Path, dst: Path, incoming_to_natives: list[mappers.Incoming2NativeMap]
) -> Path | None:
    """_summary_

    Args:
        src: File on which conversion will be attempted.
        dst: Root underneath which the mapped file will be placed.
        incoming_to_natives: List of mappings to attempt.

    Returns:
        Path | None: If a mapping was found, the mapped file, else `None`.
    """
    for mapping in incoming_to_natives:
        if mapping.src_pattern.search(str(src)):
            return mapping.map(src, outroot=dst)


def convert_flat(
    src: Path, dst: Path, incoming_to_natives: list[mappers.Incoming2NativeMap]
) -> list[Path] | list[typing.Never]:
    out = []
    for entry in src.glob("*"):
        if mapped := _attempt_map(
            entry, dst, incoming_to_natives=incoming_to_natives
        ):
            out.append(mapped)

    return out


def convert_recursively(
    src: Path, dst: Path, incoming_to_natives: list[mappers.Incoming2NativeMap]
) -> list[Path] | list[typing.Never]:
    out = []
    for r, dirs, _ in os.walk(src, topdown=False):
        root = Path(r)
        for d in dirs + [root]:
            if mapped := convert_flat(
                root / d, dst=dst, incoming_to_natives=incoming_to_natives
            ):
                out.extend(mapped)

    return out
