from pydantic import BaseModel
from pydantic.fields import Field

# You're communicating with some API that uses camelCase, but you want to use snake_case.
class User(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")

external_data = {"firstName": "Jan", "lastName": "Klaasse"}

user = User(**external_data)

print(user.first_name)
print(user.last_name)

# By default though, the following does not work.
try:
    user = User(first_name="Jan", last_name="Klaasse")
except Exception as e:
    print(e)

# Why? You cannot assign by field_name by default. We can fix this though.
class User(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    class Config:
        allow_population_by_field_name = True

user = User(first_name="Jan", last_name="Klaasse")
print(user.json())

# Adding all aliases becomes tedious for large inputs....
def to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class User(BaseModel):
    first_name: str
    last_name: str
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel

external_data = {"firstName": "Jan", "lastName": "Klaasse"}
user = User(**external_data)
print(user)