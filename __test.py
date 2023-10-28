import subprocess

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
    ["python", "bot.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
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
