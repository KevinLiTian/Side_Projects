""" Shell Script """
# pylint: disable=import-error,wrong-import-position

from klang import klang

while True:
    text = input("Klang > ")

    if text == "exit":
        break

    result, error = klang.run('<stdin>', text)

    if error:
        print(error.as_string())

    elif result:
        print(result)
