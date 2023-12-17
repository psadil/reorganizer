from stdtobids import mappers

incoming_to_native = [
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<blob>\w+)\.zip",
        repl=r"\g<blob>",
        mapper=mappers.unpack_archive,
    )
]

native_to_bids = [
    # 20227 - Resting fMRI
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<sub>\d+)_20227_(?P<ses>\d{1})_0/fMRI/rfMRI_SBREF\.(?P<ext>nii\.gz|json)\Z",
        repl=r"ses-\g<ses>/func/sub-\g<sub>_ses-\g<ses>_task-rest_sbref.\g<ext>",
        mapper=mappers.move,
    ),
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<sub>\d+)_20227_(?P<ses>\d{1})_0/fMRI/rfMRI\.(?P<ext>nii\.gz|json)\Z",
        repl=r"ses-\g<ses>/func/sub-\g<sub>_ses-\g<ses>_task-rest_bold.\g<ext>",
        mapper=mappers.move,
    ),
    # 20249 - Resting fMRI
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<sub>\d+)_20227_(?P<ses>\d{1})_0/fMRI/tfMRI_SBREF\.(?P<ext>nii\.gz|json)\Z",
        repl=r"ses-\g<ses>/func/sub-\g<sub>_ses-\g<ses>_task-hariri_sbref.\g<ext>",
        mapper=mappers.move,
    ),
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<sub>\d+)_20227_(?P<ses>\d{1})_0/fMRI/tfMRI\.(?P<ext>nii\.gz|json)\Z",
        repl=r"ses-\g<ses>/func/sub-\g<sub>_ses-\g<ses>_task-hariri_bold.\g<ext>",
        mapper=mappers.move,
    ),
    # 20252 - T1 nifti
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<sub>\d+)_20252_(?P<ses>\d{1})_0/T1/T1\.(?P<ext>nii\.gz|json)\Z",
        repl=r"ses-\g<ses>/anat/sub-\g<sub>_ses-\g<ses>_T1w.\g<ext>",
        mapper=mappers.move,
    ),
    # 25747-25755 connectivities
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"(?P<dfile>\d+_(?P<blob>\d+)_(?P<ses>\d{1})_0)\.txt",
        repl=r"ses-\g<ses>/non-bids/\g<blob>/\g<dfile>.txt",
        mapper=mappers.move,
    ),
    # remaining folders
    mappers.Incoming2NativeMap.from_str(
        src_pattern=r"\d+_(?P<blob>\d+)_(?P<ses>\d{1})_0\Z",
        repl=r"ses-\g<ses>/non-bids/\g<blob>",
        mapper=mappers.move,
    ),
]
