""" Shell Script """
# pylint: disable=import-error,wrong-import-position

from klang import klang
from klang.util import TextColors

print(f"{TextColors.OKCYAN}\nWelcome to Klang Shell!\n{TextColors.ENDC}")

while True:
    text = input("> ")

    if text == "exit":
        break

    result, error = klang.run('<stdin>', text)

    if error:
        print(error.as_string())

    elif result:
        print(result)
