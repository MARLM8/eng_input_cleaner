import sys
import os
from text_pipeline import process

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


while True:
    user_input = input("enter your text: ")

    if user_input.lower() == "exit":
        break

    result = process(user_input)
    print(result)