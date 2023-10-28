from collections import UserDict
from datetime import datetime


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
        print(f"Log3: {value}")
        date_obj = datetime.strptime(value, self.DATE_FORMAT)
        super().__init__(date_obj)

    def __lt__(self, other):
        if isinstance(other, Birthday):
            return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, Birthday):
            return self.value > other.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ["None"]

    def add_phone(self, value):
        self.phones.append(Phone(value))

    def add_birthday(self, value):
        self.birthday = [Birthday(value)]

    def find_phone(self, phone):
        try:
            res = list(filter(lambda x: x == phone, self.phones))[0]
            return res
        except:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone == old_phone:
                self.phones[idx] = Phone(new_phone)
                print(f"Phone number updated to {new_phone}")

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday[0]}"

    # def __getitem__(self, key):
    #     if key == "birthday":
    #         print(f"Log4 ")
    #         return self.birthday


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        for i in self.data:
            if i == name:
                del i
                print(f"Contact {name} has been deleted.")

    def show_birthday(self, name):
        for i in self.data:
            if i == name:
                return self.data[i].birthday[0]
            else:
                print("Contact not found")

    def birthdays(self):
        birthday_dict = {}
        for user in sorted(self.data.values(), key=lambda x: x.birthday):
            current_date = datetime.now().date()
            next_year = current_date.year + 1
            birthday = user.birthday[0]
            if birthday == "None":
                continue
            birthday = birthday.value.date()
            birthday_this_year = birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday.replace(year=next_year)

            delta_days = (birthday_this_year - current_date).days

            if delta_days < 5:
                weekday = birthday_this_year.strftime("%A")
                if weekday in ("Saturday", "Sunday"):
                    weekday = "Monday"
                if weekday in birthday_dict:
                    birthday_dict[weekday] += [user["name"]]
                else:
                    birthday_dict[weekday] = [user["name"]]
        res = "\n".join(
            f"{day}: {', '.join(names)}" for day, names in birthday_dict.items()
        )
        return res


class Bot:
    def __init__(self):
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
            # elif command == "phone":
            #     print(phone_contact(args[0], contacts))
            # elif command == "all":
            #     print(all_contact(contacts))
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

    def close_bot(self):
        print("Good bye!")

    def helloBot(self):
        print("How can I help you?")

    @_input_error
    def add_contact(self, args):
        name, phone = args
        john_record = Record(name)
        john_record.add_phone(phone)
        self.contacts.add_record(john_record)
        print("Contact added.")

    @_input_error
    def change_contact(self, args):
        name, phone = args
        contact = self.contacts.find(name)
        # contact.edit_phone("1234567890", "1112223333")


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("12.04.2002")
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print(book.show_birthday("Jane"))

    # Видалення запису Jane
    book.delete("Jane")

    # День народженя запису Jone
    print(book.show_birthday("John"))

    # Список день народжень для привітання
    print(book.birthdays())
    Bot()
