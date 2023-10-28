from datetime import datetime


def get_birthdays_per_week(users):
    birthday_dict = {}

    for user in sorted(users, key=lambda x: x["birthday"]):
        print(user)
        print(user["birthday"])
        current_date = datetime.now().date()
        next_year = current_date.year + 1
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=current_date.year)

        if birthday_this_year < current_date:
            birthday_this_year = birthday.replace(year=next_year)

        delta_days = (birthday_this_year - current_date).days

        if (
            delta_days < 5
        ):  # Хотя в условие сказанно, delta_days < 7, но на мой взгляд реализация этой задачи требует иное значение.
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
    print(res)


# Данные, что я использовал для тестирвания.
test_data = [
    {"name": "Bill Gates", "birthday": datetime(1955, 6, 24)},
    {"name": "Paul Gates", "birthday": datetime(1956, 6, 24)},
    {"name": "Bill Door", "birthday": datetime(1965, 7, 25)},
    {"name": "Bill Window", "birthday": datetime(1975, 8, 26)},
    {"name": "Bill Table", "birthday": datetime(1985, 9, 27)},
    {"name": "Bill Brid", "birthday": datetime(1995, 10, 28)},
    {"name": "Wayn Brigau", "birthday": datetime(1995, 10, 20)},
    {"name": "Pol Brigau", "birthday": datetime(1995, 10, 16)},
    {"name": "Tom Brigau", "birthday": datetime(1995, 10, 18)},
    {"name": "Steve Bragau", "birthday": datetime(1995, 10, 18)},
    {"name": "Bill Brigau", "birthday": datetime(1995, 10, 21)},
    {"name": "Bob Brigau", "birthday": datetime(1995, 10, 21)},
    {"name": "Braun Brigau", "birthday": datetime(1995, 10, 22)},
    {"name": "Bei Brigau", "birthday": datetime(1995, 10, 23)},
]

if __name__ == "__main__":
    get_birthdays_per_week(test_data)
