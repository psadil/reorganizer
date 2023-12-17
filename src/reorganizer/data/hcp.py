from reorganizer import mappers


native_to_bids = [
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"MNINonLinear\Z",
        repl=r"non-bids/MNINonLinear",
        mapper=mappers.move,
    ),
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"release-notes\Z",
        repl=r"non-bids/release-notes",
        mapper=mappers.move,
    ),
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"T1w\Z",
        repl=r"non-bids/T1w",
        mapper=mappers.move,
    ),
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"unprocessed\Z",
        repl=r"non-bids/unprocessed",
        mapper=mappers.move,
    ),
]
