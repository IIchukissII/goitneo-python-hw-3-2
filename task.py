from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number")


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        date_obj = datetime.strptime(value, self.DATE_FORMAT)
        # super().__init__(date_obj)
        super().__init__(date_obj.date())

    def __lt__(self, other):
        if isinstance(other, Birthday):
            return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, Birthday):
            return self.value > other.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = ""
        self.birthday = "None"

    def add_phone(self, value):
        self.phone = Phone(value)

    def edit_phone(self, new_phone):
        self.phone = new_phone
        return f"Phone number updated to {new_phone}"

    def __str__(self):
        return (
            f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        res = self.data.get(name)
        if res:
            return res
        else:
            print("Contact not found")

    def add_birthday(self, name, birthday):
        contact = self.find(name)
        contact.birthday = Birthday(birthday)

    def show_birthday(self, name):
        for i in self.data:
            if i == name:
                return self.data[i].birthday
            else:
                return "Contact not found"

    def birthdays(self):
        birthday_dict = {}
        for user in sorted(self.data.values(), key=lambda x: x.birthday):
            current_date = datetime.now().date()
            next_year = current_date.year + 1
            birthday = user.birthday
            if birthday == "None":
                continue
            birthday = birthday.value
            birthday_this_year = birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday.replace(year=next_year)

            delta_days = (birthday_this_year - current_date).days

            if delta_days <= 5:
                weekday = birthday_this_year.strftime("%A")
                if weekday in ("Saturday", "Sunday"):
                    weekday = "Monday"
                if weekday in birthday_dict:
                    birthday_dict[weekday] += [user.name]
                else:
                    birthday_dict[weekday] = [user.name]

        res = "\nAll Birthdays:\n"
        for day, names in birthday_dict.items():
            res += f"{day}: {', '.join(map(str, names))}\n"
        return res


class Bot:
    FILE_NAME = "data.json"

    def __init__(self):
        data = self.read_from_file()
        if not data == None:
            self.contacts = data
        else:
            self.contacts = AddressBook()
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
        with open(self.FILE_NAME, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_from_file(self):
        try:
            with open(self.FILE_NAME, "rb") as file:
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
    Bot()
