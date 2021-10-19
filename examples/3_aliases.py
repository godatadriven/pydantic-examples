#%%
from pydantic import BaseModel
from pydantic.fields import Field

from rich import print
from rich.traceback import install

install(show_locals=False)  # pretty print errors

#%% You're communicating with some API that uses camelCase, but you want to use snake_case.
class User(BaseModel):
    first_name: str
    last_name: str


external_data = {"firstName": "Jan", "lastName": "Klaasse"}

user = User(**external_data)  # <-- this fails!

#%% We can fix that with field aliases
class User(BaseModel):
    first_name: str = Field(alias="firstName")  # <-- The Fix!
    last_name: str = Field(alias="lastName")  # <-- The Fix!


user = User(**external_data)
print(f"{user=}")

#%% Now we have a new problem. Now this won't work:
user = User(first_name="Jan", last_name="Klaasse")  # <-- This fails!

# %%Why? You cannot assign by field_name by default. We can fix this though.
class User(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

    class Config:
        allow_population_by_field_name = True  # <- The Fix!


user = User(first_name="Jan", last_name="Klaasse")
print(f"{user=}")

#%% Adding all aliases becomes tedious for large inputs....
def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class User(BaseModel):
    first_name: str  # <-- Look no more Field aliases!
    last_name: str

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case  # <-- The Fix!


user = User(**external_data)
print(f"{user=}")

#%% you can also export by alias or by the attribute name
print(f"{user.dict(by_alias=False)=}")
print(f"{user.dict(by_alias=True)=}")
