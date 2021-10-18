# %%
from typing import List
from rich import print

from pydantic import BaseModel, validator, ValidationError

# %%
# In the basic example we already saw some standard input validation:
class ClassWithList(BaseModel):
    names: List

print(ClassWithList(names="no_list"))

# %%
# But we can do more fancier stuff:
# Based on: https://pydantic-docs.helpmanual.io/usage/validators/
class UserModel(BaseModel):
    name: str
    username: str
    password1: str
    password2: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v
# %%
user = UserModel(
    name='samuel colvin',
    username='scolvin',
    password1='zxcvbn',
    password2='zxcvbn',
)
print(user)

# %%
user = UserModel(
    name='samuelcolvin',
    username='sco-lvin',
    password1='zxcvbn',
    password2='zsxcvbn',
)
# %% 
# QUIRK: The order in which you define your fields matters:
class UserModel(BaseModel):
    name: str
    username: str
    password2: str
    password1: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if v != values['password1']:
            raise ValueError('passwords do not match')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


# %%
user = UserModel(
    name='samuel colvin',
    username='scolvin',
    password1='zxcvbn',
    password2='zxcvbn',
)