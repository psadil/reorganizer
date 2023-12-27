# reorganizer

-----

## Table of Contents

- [Installation](#installation)
- [About](#about)
- [Alternatives and Inspirations](#alternatives-and-inspirations)

## Installation

```console
pip install git+https://github.com/psadil/reorganizer.git@main
```

## About

This package provides a strategy for reorganizing files. The package was developed for use with neuroimaging standards. The field is blessed with many frameworks for analyzing data, but most frameworks have different standards. And new analyses often outpace the ability for the standards to evolve.

Tke stratgy files on the `Incoming2NativeMap` objects. These objects define

- regex patterns that match files to transform
- regex replacements
- a function for dealing with the files

For example, considering this object

```python
Incoming2NativeMap.from_str(
        src_pattern=r"\d+_(?P<blob>\d+)_(?P<ses>\d{1})_0\Z",
        repl=r"ses-\g<ses>/non-bids/\g<blob>",
        mapper=mappers.move,
    )
```

This is one of the elements for handling an item from the UKB. The object will match folders like `"1000043_20252_2_0"`, which is the T1w files provided for sub 1000043 during their second visit. The output will be named `"ses-2/non-bids/20252"`, and it will be converted with the `mappers.move`.

The mappers could be used by themselves. But for a few common approaches to using them are provided in [src/reorganizer/convert.py].

## Alternatives and Inspirations

- [file-mapper](https://github.com/DCAN-Labs/file-mapper). This evolved [from a BEP](https://bids.neuroimaging.io/get_involved.html#extending-the-bids-specification). If you're looking for an official tool, you should probably consult the file-mapper.
- [datalad-ukbiobank](https://github.com/datalad/datalad-ukbiobank). This project started as a modification to this datalad extension, but more flexibility was wanted (flexibility in methods of copying/renaming and flexibility in creating new mappings).
