# Pydantic provides a nice way of loading in configurations from env vars
# storing config in env vars is recommended by https://12factor.net/config

# inspiration:
# https://pydantic-docs.helpmanual.io/usage/settings/
# https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html

# exercise for the reader
# run export ENV="PRO" and rerun the file
from functools import cache
import os
from typing import Optional, Set

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, PostgresDsn, PyObject, RedisDsn
from rich import print
from rich.traceback import install

install(show_locals=False)
load_dotenv()


class GlobalConfig(BaseSettings):
    # Arguments passed to the Settings class initialiser.
    # Environment variables, e.g. my_prefix_special_function as described above.
    # Variables loaded from a dotenv (.env) file.
    # Variables loaded from the secrets directory.
    # The default field values for the Settings model.

    ENV: Optional[str] = Field(None, env="ENV")
    AUTH_KEY: str
    API_KEY: str

    REDIS_DSN: RedisDsn = "redis://user:pass@localhost:6379/1"
    PG_DSN: PostgresDsn = "postgres://user:pass@localhost:5432/foobar"

    SPECIAL_FUNCTION: PyObject = "math.cos"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    DOMAINS: Set[str] = set()

    class Config:
        env_prefix = os.environ["ENV"] + "_"  # defaults to no prefix, i.e. ""


@cache
def load_config():
    return GlobalConfig()


CONFIG = load_config()

if __name__ == "__main__":
    print(CONFIG)
