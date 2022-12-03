import telebot
import crud as cr
import logger as lg
import config
import logging

bot = telebot.TeleBot(config.Calc_bot_token)

py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, f'Hello, *{message.from_user.first_name}!*\nYou need enter:\n1) /calculator if you need calculator\n2)/help to call help\n3)To bring up the main menu, enter /main')

@bot.message_handler(commands=['calculator'])
def getMessage(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, f'''/start - start over (restart bot)\n/main - main menu\n/help - call help''')

name_it = ''
surname_it = ''
number_it = ''
email_it = ''
user_id_it = ''
new_number_it = ''

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == '/main':
        bot.send_message(message.chat.id, f'''Select a menu item by entering the command:\n 
                                        /1 - Show all contacts\n
                                        /2 - Find an contact by surname\n
                                        /3 - Find an contact by name\n
                                        /4 - Search an contact by phone number\n
                                        /5 - Add new contact\n
                                        /6 - Edit an existing contact\n
                                        /7 - Delete contact''')
        cr.init_data_base('base_phone.csv')

    elif message.text == '/1':
        lg.logging.info('The user has selected item number 1')
        bot.send_message(message.chat.id, f'{cr.retrive()}')

    elif message.text == '/2':
        lg.logging.info('The user has selected item number 2')
        bot.send_message(message.chat.id, f'Add surname')
        bot.register_next_step_handler(message, find_surname)

    elif message.text == '/3':
        lg.logging.info('The user has selected item number 3')
        bot.send_message(message.chat.id, f'Add name')
        bot.register_next_step_handler(message, find_name)

    elif message.text == '/4':
        lg.logging.info('The user has selected item number 4')
        bot.send_message(message.chat.id, f'Add phone number')
        bot.register_next_step_handler(message, find_number)

    elif message.text == '/5':
        lg.logging.info('The user has selected item number 5')
        bot.send_message(message.chat.id, f'Enter name')
        bot.register_next_step_handler(message, get_name)

    elif message.text == '/6':
        lg.logging.info('The user has selected item number 6')
        bot.send_message(
            message.chat.id, f'''Which contact do you want to change?\n
            Specify by:\n
            /61 - surname\n
            /62 - name\n
            /63 - phone number''')
        bot.register_next_step_handler(message, edit_entry)

    elif message.text == '/7':
        lg.logging.info('The user has selected item number 7')
        bot.send_message(
            message.chat.id, f'''Select the contact you want to delete?\n
            Specify by:\n
            /71 - surname\n
            /72 - name\n
            /73 - phone number''')
        bot.register_next_step_handler(message, delete_contact)

    else:
        bot.send_message(
            message.chat.id, f'I do not understund you. Please enter: /help')


def find_surname(message):
    global surname_it
    surname_it = message.text
    lg.logging.info('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(surname=surname_it)}')


def find_name(message):
    global name_it
    name_it = message.text
    lg.logging.info('User entered: {name_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(name=name_it)}')


def find_number(message):
    global number_it
    number_it = message.text
    lg.logging.info('User entered: {number_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(number=number_it)}')


def get_name(message):
    global name_it
    name_it = message.text
    lg.logging.info('User entered: {name_it}')
    bot.send_message(message.chat.id, f'Add surname')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname_it
    surname_it = message.text
    lg.logging.info('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'Add phone number')
    bot.register_next_step_handler(message, get_number)


def get_number(message):
    global number_it
    number_it = message.text
    lg.logging.info('User entered: {number_it}')
    bot.send_message(message.chat.id, f'Add email')
    bot.register_next_step_handler(message, get_email)


def get_email(message):
    global email_it
    email_it = message.text
    lg.logging.info('User entered: {email_it}')
    cr.create(name_it, surname_it, number_it, email_it)
    bot.send_message(message.chat.id, f'Contact added successfully!')


def edit_entry(message):
    if message.text == '/61':
        lg.logging.info('The user has selected item number 6.1')
        bot.send_message(message.chat.id, f'Add surname')
        bot.register_next_step_handler(message, change_surname)

    elif message.text == '/62':
        lg.logging.info('The user has selected item number 6.2')
        bot.send_message(message.chat.id, f'Add name')
        bot.register_next_step_handler(message, change_name)

    elif message.text == '/63':
        lg.logging.info('The user has selected item number 6.3')
        bot.send_message(message.chat.id, f'Add phone number')
        bot.register_next_step_handler(message, change_num)

    else:
        bot.send_message(
            message.chat.id, f'I do not understund you. Please enter: /help')


def change_name(message):
    global name_it
    name_it = message.text
    lg.logging.info('User entered: {name_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(name=name_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to change')
    bot.register_next_step_handler(message, change_number)


def change_surname(message):
    global surname_it
    surname_it = message.text
    lg.logging.info('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(surname=surname_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to change')
    bot.register_next_step_handler(message, change_number)


def change_num(message):
    global number_it
    number_it = message.text
    lg.logging.info('User entered: {number_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(number=number_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to change')
    bot.register_next_step_handler(message, change_number)


def change_number(message):
    global user_id_it
    user_id_it = message.text
    lg.logging.info('User entered: {user_id_it}')
    bot.send_message(
        message.chat.id, f'Enter a new phone number')
    bot.register_next_step_handler(message, change_new_number)


def change_new_number(message):
    global new_number_it
    new_number_it = message.text
    lg.logging.info('User entered: {new_number_it}')
    cr.update(id=user_id_it, new_number=new_number_it)
    bot.send_message(
        message.chat.id, f'Contact successfully changed!')


def delete_contact(message):
    if message.text == '/71':
        lg.logging.info('The user has selected item number 7.1')
        bot.send_message(message.chat.id, f'Add surname')
        bot.register_next_step_handler(message, delete_surname)

    elif message.text == '/72':
        lg.logging.info('The user has selected item number 7.2')
        bot.send_message(message.chat.id, f'Add name')
        bot.register_next_step_handler(message, delete_name)

    elif message.text == '/73':
        lg.logging.info('The user has selected item number 7.3')
        bot.send_message(message.chat.id, f'Add phone number')
        bot.register_next_step_handler(message, delete_num)

    else:
        bot.send_message(
            message.chat.id, f'I do not understand you. Enter: /help')


def delete_surname(message):
    global surname_it
    surname_it = message.text
    lg.logging.info('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(surname=surname_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to delete')
    bot.register_next_step_handler(message, delete_number)


def delete_name(message):
    global name_it
    name_it = message.text
    lg.logging.info('User entered: {name_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(name=name_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to delete')
    bot.register_next_step_handler(message, delete_number)


def delete_num(message):
    global number_it
    number_it = message.text
    lg.logging.info('User entered: {number_it}')
    bot.send_message(message.chat.id, f'{cr.retrive(number=number_it)}')
    bot.send_message(
        message.chat.id, f'Enter the id of the contact you want to delete')
    bot.register_next_step_handler(message, delete_number)


def delete_number(message):
    global user_id_it
    user_id_it = message.text
    lg.logging.info('User entered: {user_id_it}')
    cr.delete(id=user_id_it)
    bot.send_message(
        message.chat.id, f'Contact successfully deleted!')


value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                telebot.types.InlineKeyboardButton('c', callback_data='c'),
                telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                telebot.types.InlineKeyboardButton('/', callback_data='/') )

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'),
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*') )

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='7'),
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-') )

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'),
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+') )

keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data=','),
                telebot.types.InlineKeyboardButton('=', callback_data='=') )


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data

    if data == 'no':
        pass
    elif data == 'c':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        logging.info("The data == =")
        try:
            value = str( eval(value) )
            logging.info(f"The value result: {str( eval(value) )}.")
        except:
            value = 'Error!'
            logging.error("Error!",exc_info=True)
    else:
        value += data
        
    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id, text='0', reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id, text=value, reply_markup=keyboard)
            old_value = value
    
    if value == 'Error!': value = ''



print('server start')

bot.polling(none_stop=False, interval=0)
