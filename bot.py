import telebot
from telebot import types
import buttons
import database

bot = telebot.TeleBot('8198591781:AAFgA21EQ30eJOS9CFjkRRuWkKQ-Apdzi3k')  # Replace 'YOUR_BOT_TOKEN' with your actual token
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if database.check_user(user_id):  # Check if the user is already registered
        bot.send_message(user_id, f"Добро пожаловать, @{message.from_user.username}!")
        bot.send_message(user_id, 'Выберите пункт:', reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(user_id, "Привет! Давай начнем регистрацию!", reply_markup=keyboard)
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_name = message.text

    users[user_id] = {'name': user_name, 'pr_count': 0, 'pr_name': None}  # Initialize user data
    bot.send_message(user_id, 'Отлично! Теперь отправьте ваш номер телефона.', reply_markup=buttons.num_button())
    bot.register_next_step_handler(message, get_num)

@bot.callback_query_handler(func=lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_count(call):
    user_id = call.message.chat.id

    if user_id not in users:
        users[user_id] = {'pr_count': 0, 'pr_name': None}

    if call.data == 'increment':
        users[user_id]['pr_count'] += 1
    elif call.data == 'decrement' and users[user_id]['pr_count'] > 0:
        users[user_id]['pr_count'] -= 1
    elif call.data == 'to_cart':
        pr_name = users[user_id]['pr_name']
        pr_count = users[user_id]['pr_count']
        database.add_to_cart(user_id, pr_name, pr_count)
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, "Товар помещен в корзину! Желаете что-то еще?",
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
        return
    elif call.data == 'back':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Переношу вас обратно...', reply_markup=buttons.main_menu(database.get_pr_buttons()))
        return

    bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=call.message.message_id,
        reply_markup=buttons.choose_amount(
            database.get_exact_pr(users[user_id]['pr_name'])[4],
            call.data,
            users[user_id]['pr_count']
        )
    )

@bot.callback_query_handler(func=lambda call: call.data in ['order', 'clear', 'cart'])
def cart_handle(call):
    user_id = call.message.chat.id
    if call.data == 'cart':
        cart_items = database.show_cart(user_id)
        if not cart_items:
            bot.send_message(user_id, "Ваша корзина пуста!")
            return
        text = "Ваша корзина:\n\n"
        total = 0
        for item in cart_items:
            text += f"Товар: {item[1]} | Количество: {item[2]}\n"
            total += database.get_exact_price(item[1]) * item[2]
        text += f"\nИтого: {total} сум"
        bot.send_message(user_id, text, reply_markup=buttons.cart_buttons())
    elif call.data == 'clear':
        database.clear_cart(user_id)
        bot.send_message(user_id, "Корзина очищена.", reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'order':
        bot.send_message(user_id, "Отправьте локацию для доставки.", reply_markup=buttons.loc_button())
        bot.register_next_step_handler(call.message, get_location)

def get_location(message):
    user_id = message.from_user.id
    if message.location:
        bot.send_message( f"Новый заказ от @{message.from_user.username}.")
        bot.send_location( latitude=message.location.latitude, longitude=message.location.longitude)
        database.make_order(user_id)
        bot.send_message(user_id, "Ваш заказ принят. Ожидайте!", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Пожалуйста, отправьте локацию!")

def get_num(message):
    user_id = message.from_user.id
    if message.contact and message.contact.user_id == user_id:
        user_num = message.contact.phone_number
        database.register(user_id, users[user_id]['name'], user_num)
        bot.send_message(user_id, "Спасибо за регистрацию!", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт:', reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, "Пожалуйста, отправьте номер телефона.")
        bot.register_next_step_handler(message, get_num)

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    user_id = message.from_user.id
    if message.text in database.get_pr_buttons():
        product = database.get_product_info(message.text)
        if product:
            name, description, image = product
            bot.send_photo(
                user_id,
                image,
                caption=f"*{name}*\n{description}\nЦена: {database.get_exact_price(name)} сум",
                reply_markup=buttons.choose_amount(database.get_exact_price(name), 'increment', 1)
            )

bot.polling(none_stop=True)
