""" Shell Script """
import basic

while True:
    text = input("Klang > ")
    result, error = basic.run('<stdin>', text)

    if error:
        print(error.as_string())

    else:
        print(result)
