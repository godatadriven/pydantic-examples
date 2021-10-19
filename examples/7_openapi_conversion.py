# TODO(Daniel)
# %%
# Generate a model from an example json.
# datamodel-codegen --input-file-type json --input example.json --output menu.py

# %% 
import json
from menu import Model

menu = Model.parse_file("example.json")

print(menu)