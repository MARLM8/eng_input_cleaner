from eng_input_cleaner import process

while True:
    user_input = input("enter your text: ")

    if user_input.lower() == "exit":
        break

    result = process(user_input)
    print(result)