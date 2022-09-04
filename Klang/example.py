""" Example Klang Program """
from klang import klang

with open("example.txt") as file:
    contents = file.read()
    klang.run('<program>', contents)
