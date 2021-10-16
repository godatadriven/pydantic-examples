# Example from: https://pydantic-docs.helpmanual.io
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from rich import print
from rich.traceback import install

install(show_locals=True)

# Pydantic is useful to get data from external sources, such as API's.
# It can do data validation and can enforce type hints.


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: Optional[List[int]] = None


@dataclass
class DataClassUser:
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: Optional[List[int]] = None


external_data = {
    "id": "123",
    "signup_ts": "2019-06-01 12:22",
    "friends": [1, 2, "3"],
}

user = User(**external_data)
data_class_user = DataClassUser(**external_data)

print("string:", user)
print("json:", user.json())
print(data_class_user)


# It enforces type hints (but also does automatic conversions...)
external_data_broken = {
    "id": [123, 456],
    "signup_ts": "2019-06-01 12:22",
    "friends": [1, 2, "3"],
}
data_class_user = DataClassUser(**external_data_broken)
print(data_class_user)

user_broken = User(**external_data_broken)
