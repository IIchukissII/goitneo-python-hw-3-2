import pickle
from task import AddressBook, Record

contacts = {}


def _parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def _input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me 'name' and 'phone'."
        except TypeError:
            return "Give me only 'name'."

    return inner


def save_to_file(filename):
    with open(filename, "wb") as file:
        pickle.dump(contacts, file)


def read_from_file(filename):
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        return None


def close_bot(filename):
    save_to_file(filename)
    print("Good bye!")


def helloBot():
    print("How can I help you?")


@_input_error
def add_contact(args):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    print("Contact added.")


@_input_error
def change_contact(args):
    name, phone = args
    contact = contacts.find(name)
    res = contact.edit_phone(phone)
    print(res)


@_input_error
def phone_contact(args):
    name = args[0]
    contact = contacts.find(name)
    phone = contact.phone
    print(phone)


def all_contact():
    res = "\nAll Contacts:\n"
    for key, value in contacts.items():
        res += f"{key}: {value}\n"
    print(res)


@_input_error
def add_birthday(args):
    name, birthday = args
    contacts.add_birthday(name, birthday)


@_input_error
def show_birthday(args):
    name = args[0]
    contact = contacts.find(name)
    birthday = contact.birthday
    print(birthday)


def birthdays():
    birthdays = contacts.birthdays()
    print(birthdays)


def main(filename):
    global contacts
    data = read_from_file(filename)
    if not data == None:
        contacts = data
    else:
        contacts = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = _parse_input(user_input)

        if command in ["good bye", "close", "exit"]:
            close_bot(filename)
            break
        elif command == "hello":
            helloBot()
        elif command == "add":
            add_contact(args)
        elif command == "change":
            change_contact(args)
        elif command == "phone":
            phone_contact(args)
        elif command == "all":
            all_contact()
        elif command == "add-birthday":
            add_birthday(args)
        elif command == "show-birthday":
            show_birthday(args)
        elif command == "birthdays":
            birthdays()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main("data.json")
