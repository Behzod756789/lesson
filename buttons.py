
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def choose_amount(pr_amount, plus_or_minus, amount):
    kb = InlineKeyboardMarkup(row_width=3)

    if plus_or_minus == 'increment' and amount < pr_amount:
        plus = InlineKeyboardButton(text=str(amount + 1), callback_data=f'increment_{amount + 1}')
    else:
        plus = InlineKeyboardButton(text='-', callback_data='none')  # Disable if max reached

    if amount > 1:
        minus = InlineKeyboardButton(text=str(amount - 1), callback_data=f'decrement_{amount - 1}')
    else:
        minus = InlineKeyboardButton(text='-', callback_data='none')  # Disable if min reached

    count = InlineKeyboardButton(text=f"Количество: {amount}", callback_data='none')

    to_cart = InlineKeyboardButton(text='🛒 В корзину', callback_data='to_cart')
    back = InlineKeyboardButton(text='↩️ Назад', callback_data='back')

    kb.add(minus, count, plus)
    kb.row(back, to_cart)

    return kb

def cart_buttons():
    kb = InlineKeyboardMarkup(row_width=2)

    order = InlineKeyboardButton(text='📦 Оформить заказ', callback_data='order')
    clear = InlineKeyboardButton(text='🗑️ Очистить корзину', callback_data='clear')
    back = InlineKeyboardButton(text='↩️ Назад', callback_data='back')

    kb.add(order, clear)
    kb.row(back)

    return kb

def admin_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    but1 = KeyboardButton('Добавить продукт')
    but2 = KeyboardButton('Удалить продукт')
    but3 = KeyboardButton('Изменить продукт')
    but4 = KeyboardButton('Перейти в главное меню')

    kb.add(but1, but2, but3)
    kb.row(but4)

    return kb

def num_button():

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_button = KeyboardButton("📞 Отправить номер телефона", request_contact=True)
    keyboard.add(phone_button)
    return keyboard
