try:
    user_input = input("Будь ласка, введіть число: ")
    number = int(user_input)
    print(f"Успішно конвертовано! Ваше ціле число: {number}")
except ValueError:
    print("Помилка! Введені дані не можна конвертувати в ціле число.")