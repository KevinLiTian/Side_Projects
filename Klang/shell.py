""" Shell Script """
# pylint: disable=import-error,wrong-import-position

from Basic.basic import run

while True:
    text = input("Klang > ")

    if text == "exit":
        break

    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())

    else:
        print(result)
