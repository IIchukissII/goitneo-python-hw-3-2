def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me 'name' and 'phone'."
        except TypeError:
            return "Give me only 'name'."

    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        return "Contact not found"


@input_error
def phone_contact(username, contacts):
    if username in contacts:
        return f"Phone of {username}: {contacts[username]}"
    else:
        return "Contact not found"


def all_contact(contacts):
    res = "\nAll phones:\n"
    for key, value in contacts.items():
        res += f"{key}: {value}\n"
    return res


def helloBot():
    print("How can I help you?")


def close_bot():
    print("Good bye!")


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["good bye", "close", "exit"]:
            close_bot()
            break
        elif command == "hello":
            helloBot()
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(phone_contact(args[0], contacts))
        elif command == "all":
            print(all_contact(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
