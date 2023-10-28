import subprocess

# data = [
#     {"name": "Bill Gates", "birthday": datetime(1955, 6, 24)},
#     {"name": "Paul Gates", "birthday": datetime(1956, 6, 24)},
#     {"name": "Bill Door", "birthday": datetime(1965, 7, 25)},
#     {"name": "Bill Window", "birthday": datetime(1975, 8, 26)},
#     {"name": "Bill Table", "birthday": datetime(1985, 9, 27)},
#     {"name": "Bill Brid", "birthday": datetime(1995, 10, 28)},
#     {"name": "Wayn Brigau", "birthday": datetime(1995, 10, 20)},
#     {"name": "Pol Brigau", "birthday": datetime(1995, 10, 16)},
#     {"name": "Tom Brigau", "birthday": datetime(1995, 10, 18)},
#     {"name": "Steve Bragau", "birthday": datetime(1995, 10, 18)},
#     {"name": "Bill Brigau", "birthday": datetime(1995, 10, 21)},
#     {"name": "Bob Brigau", "birthday": datetime(1995, 10, 21)},
#     {"name": "Braun Brigau", "birthday": datetime(1995, 10, 22)},
#     {"name": "Bei Brigau", "birthday": datetime(1995, 10, 23)},
# ]

# Список команд для выполнения
commands = [
    "add Bill-Gates 1234567890",
    "add-birthday Bill-Gates 24.6.1955",
    "add Paul-Gates 1234567890",
    "add-birthday Paul-Gates 24.6.1956",
    "add Bill-Door 1234567890",
    "add-birthday Bill-Door 25.7.1965",
    "add Bill-Window 1234567890",
    "add-birthday Bill-Window 26.8.1975",
    "add Bill-Table 1234567890",
    "add-birthday Bill-Table 27.9.1985",
    "add Bill-Brid 1234567890",
    "add-birthday Bill-Brid 28.10.1995",
    "add Wayn-Brigau 1234567890",
    "add-birthday Wayn-Brigau 29.10.1995",
    "add Pol-Brigau 1234567890",
    "add-birthday Pol-Brigau 30.10.1995",
    "add Tom-Brigau 1234567890",
    "add-birthday Tom-Brigau 31.10.1995",
    "add Steve-Bragau 1234567890",
    "add-birthday Steve-Bragau 1.11.1995",
    "add Bill-Brigau 1234567890",
    "add-birthday Bill-Brigau 2.11.1995",
    "add Bob-Brigau 1234567890",
    "add-birthday Bob-Brigau 2.11.1995",
    "add Braun-Brigau 1234567890",
    "add-birthday Braun-Brigau 3.11.1995",
    "add Bei-Brigau 1234567890",
    "add-birthday Bei-Brigau 3.11.1995",
    "add Bei-Sut 1234567890",
    "add-birthday Bei-Sut 4.11.1995",
    "add Bei-Sun 1234567890",
    "add-birthday Bei-Sun 5.11.1995",
    "all",
    "birthdays",
    "close",
]

# Запуск бота и передача команд
bot_process = subprocess.Popen(
    ["python", "task.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)

for command in commands:
    bot_process.stdin.write(command + "\n")
    bot_process.stdin.flush()

# Завершение взаимодействия с ботом
bot_process.stdin.write("close\n")
bot_process.stdin.flush()

# Получение вывода бота
output, _ = bot_process.communicate()

print(output)
