""" Shell Script """
# pylint: disable=import-error,wrong-import-position

from klang import klang
from klang.util import TextColors

print(f"{TextColors.OKCYAN}\nWelcome to Klang Shell!{TextColors.ENDC}")
print("Type 'exit' or press 'control + c' to exit shell")

while True:
    text = input("> ")

    if text == "exit":
        break

    result, error = klang.run('<stdin>', text)

    if error:
        print(error.as_string())

    elif result:
        print(result)
