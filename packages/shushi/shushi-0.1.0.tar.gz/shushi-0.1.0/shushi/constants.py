import os
import pathlib

_appdata_base = (
    pathlib.Path(os.environ.get("SHUSHI_DATA", os.environ.get("appdata")))
)
APPDATA = _appdata_base.joinpath("shushi")

for p in [APPDATA]:
    p.mkdir(exist_ok=True)
