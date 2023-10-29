import pickle
from task import AddressBook, Record


class Bot:
    def __init__(self, filename):
        self.filename = filename
        data = self.read_from_file()
        if not data == None:
            self.contacts = data
        else:
            self.contacts = AddressBook()

    def run(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = self._parse_input(user_input)

            if command in ["good bye", "close", "exit"]:
                self.close_bot()
                break
            elif command == "hello":
                self.helloBot()
            elif command == "add":
                self.add_contact(args)
            elif command == "change":
                self.change_contact(args)
            elif command == "phone":
                self.phone_contact(args)
            elif command == "all":
                self.all_contact()
            elif command == "add-birthday":
                self.add_birthday(args)
            elif command == "show-birthday":
                self.show_birthday(args)
            elif command == "birthdays":
                self.birthdays()
            else:
                print("Invalid command.")

    def _parse_input(self, user_input):
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

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_from_file(self):
        try:
            with open(self.filename, "rb") as file:
                data = pickle.load(file)
                return data
        except FileNotFoundError:
            return None

    def close_bot(self):
        self.save_to_file()
        print("Good bye!")

    def helloBot(self):
        print("How can I help you?")

    @_input_error
    def add_contact(self, args):
        name, phone = args
        record = Record(name)
        record.add_phone(phone)
        self.contacts.add_record(record)
        print("Contact added.")

    @_input_error
    def change_contact(self, args):
        name, phone = args
        contact = self.contacts.find(name)
        res = contact.edit_phone(phone)
        print(res)

    @_input_error
    def phone_contact(self, args):
        name = args[0]
        contact = self.contacts.find(name)
        phone = contact.phone
        print(phone)

    def all_contact(self):
        res = "\nAll Contacts:\n"
        for key, value in self.contacts.items():
            res += f"{key}: {value}\n"
        print(res)

    @_input_error
    def add_birthday(self, args):
        name, birthday = args
        self.contacts.add_birthday(name, birthday)
        print("Birthday added.")

    @_input_error
    def show_birthday(self, args):
        name = args[0]
        contact = self.contacts.find(name)
        birthday = contact.birthday
        print(birthday)

    def birthdays(self):
        birthdays = self.contacts.birthdays()
        print(birthdays)


if __name__ == "__main__":
    bot = Bot("data.json")
    bot.run()
