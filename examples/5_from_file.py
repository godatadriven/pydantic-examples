# TODO(Rens)
from __future__ import annotations

import datetime
import json
import tempfile
from pathlib import Path
from typing import List, Optional, Union

import yaml
from pydantic import BaseModel
from rich import print
from rich.traceback import install

install(show_locals=False)

# Usecase: load settings from a yaml file.
class DayOff(BaseModel):
    date: datetime.date
    reason: Optional[str] = None


class MyParams(BaseModel):
    name: str
    days_off: List[DayOff]

    @classmethod
    def from_fpath(cls, fpath: Union[str, Path]) -> MyParams:
        fpath = Path(fpath)
        params_txt = fpath.read_text()
        if fpath.suffix == ".json":
            params_dict = json.loads(params_txt)
        elif fpath.suffix in (".yaml", "yml"):
            params_dict = yaml.safe_load(params_txt)
        else:
            raise ValueError(
                f"Only .json and .y(a)ml are supported. Got {fpath.suffix=}"
            )

        return cls.parse_obj(params_dict)


#%% try
inputs = {
    "name": "Rens Dimmendaal",
    "days_off": [
        {"date": "2021-11-30", "reason": "friends visiting amsterdam"},
        {"date": "2022-01-01", "reason": "new year day"},
        {"date": "2022-02-01", "reason": "First of February"},
    ],
}

# %%

with tempfile.TemporaryDirectory("w") as td:
    # save yaml to file
    fpath = Path(td) / "my_params.yaml"
    with open(fpath, "w") as f:
        yaml.safe_dump(inputs, f)
    assert fpath.exists()

    # What we all do it for...
    my_params = MyParams.from_fpath(fpath)
    print(my_params)
