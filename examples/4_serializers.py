# From: https://stackoverflow.com/questions/66548586/how-to-change-date-format-in-pydantic

from datetime import datetime, timezone
from pydantic import BaseModel, validator


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)


class DateTimeClass(BaseModel):
    datetime_start: datetime

    # custom input conversion for that field
    @validator("datetime_start")
    def convert_to_utc(cls, v):
        return transform_to_utc_datetime(v)

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


special_datetime = DateTimeClass(datetime_start="2042-3-15T12:45+01:00")  # note the different timezone

# input conversion
print(special_datetime.datetime_start)  # 2042-03-15 11:45:00+00:00

# output conversion
print(special_datetime.json())  # {"datetime_start": "2042-03-15T11:45:00Z"}
