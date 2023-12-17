from pathlib import Path
import string
import shutil
import tempfile

import pytest
import hypothesis
from hypothesis import strategies as st

from reorganizer.data import ukb
from reorganizer import convert


PATH_ALPHABET = string.ascii_letters + string.digits + "._-/"


@hypothesis.given(st.data())
def test_ukb_flat(data: st.DataObject):
    with tempfile.TemporaryDirectory() as tmp_src, tempfile.TemporaryDirectory() as tmp_dst:
        src = Path(tmp_src)
        dst = Path(tmp_dst)
        for mapping in ukb.incoming_to_native:
            file = Path(
                data.draw(
                    st.from_regex(
                        mapping.src_pattern,
                        fullmatch=True,
                        alphabet=PATH_ALPHABET,
                    )
                )
            )

            if any(
                f[0] in file.suffix.removeprefix(".")
                for f in shutil.get_archive_formats()
            ):
                with tempfile.TemporaryDirectory(dir=tmp_src) as z:
                    (Path(z) / "file.nii.gz").touch()
                    shutil.make_archive(
                        src / file.stem,
                        file.suffix.removeprefix("."),
                        z,
                    )
            else:
                (src / file).touch()

        out = convert.convert_flat(src, dst, ukb.incoming_to_native)

        any_out = len(out) > 0
        every_out_exists = all([f.exists() for f in out])

        assert all([any_out, every_out_exists])


@hypothesis.given(st.data())
def test_ukb_recursive(data: st.DataObject):
    with tempfile.TemporaryDirectory() as tmp_path:
        src = Path(tmp_path) / "src"
        dst = Path(tmp_path) / "dst"
        for mapping in ukb.native_to_bids:
            file = Path(
                data.draw(
                    st.from_regex(
                        mapping.src_pattern,
                        fullmatch=True,
                        alphabet=PATH_ALPHABET,
                    )
                )
            )
            if not file.suffix:
                (src / file).mkdir(parents=True, exist_ok=True)
                (src / file / "file.txt").touch()
            else:
                tocreate = src / file
                if not (parent := tocreate.parent).exists():
                    parent.mkdir(parents=True, exist_ok=True)
                tocreate.touch()

        out = convert.convert_recursively(src, dst, ukb.native_to_bids)

        any_out = len(out) > 0
        every_out_exists = all([f.exists() for f in out])

        assert all([any_out, every_out_exists])


@pytest.mark.parametrize(
    "infile,outfile",
    [
        (
            Path("1000043_20227_2_0/fMRI/rfMRI.json"),
            Path("ses-2/func/sub-1000043_ses-2_task-rest_bold.json"),
        ),
        (
            Path("1000043_20227_2_0/fMRI/rfMRI.nii.gz"),
            Path("ses-2/func/sub-1000043_ses-2_task-rest_bold.nii.gz"),
        ),
        (
            Path("1000043_20227_2_0/fMRI/rfMRI_SBREF.nii.gz"),
            Path("ses-2/func/sub-1000043_ses-2_task-rest_sbref.nii.gz"),
        ),
        (
            Path("1000043_20252_2_0/T1/T1.nii.gz"),
            Path("ses-2/anat/sub-1000043_ses-2_T1w.nii.gz"),
        ),
    ],
)
def test_ukb2bids_explicit(tmp_path: Path, infile: Path, outfile: Path):
    """Test that known inputs go to expected outputs for ukb mapping"""
    src = tmp_path / "src"
    dst = tmp_path / "dst"

    if not infile.suffix:
        (src / infile).mkdir(parents=True, exist_ok=True)
    else:
        tocreate = src / infile
        if not (parent := tocreate.parent).exists():
            parent.mkdir(parents=True, exist_ok=True)
        tocreate.touch()

    convert.convert_recursively(src, dst, ukb.native_to_bids)

    assert (dst / outfile).exists()
