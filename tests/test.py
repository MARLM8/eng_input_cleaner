from eng_input_cleaner import process
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

while True:
    user_input = input("enter your text: ")

    if user_input.lower() == "exit":
        break

    result = process(user_input)
    print(result)