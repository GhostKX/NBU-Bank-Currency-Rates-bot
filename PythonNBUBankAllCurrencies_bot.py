import telebot
import buttons
import requests
from datetime import datetime
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Welcome to the 🏦 NBU exchange rates bot!',
                     reply_markup=buttons.start_bot_buttons())
    bot.register_next_step_handler(message, user_choice)


currencies = []


def user_choice(message):
    user_id = message.from_user.id
    if message.text == '📈 Exchange rates':
        url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
        if url.status_code == 200:
            currency_data = url.json()
            initial_date = currency_data[-1]['date']
            date = datetime.strptime(initial_date, '%d.%m.%Y %H:%M:%S')
            structured_date = date.strftime('%d of %B, %Y')
            currencies = [
                ("💵 USD", currency_data[-1]['nbu_buy_price'], currency_data[-1]['nbu_cell_price']),
                ("💶 EUR", currency_data[7]['nbu_buy_price'], currency_data[7]['nbu_cell_price']),
                ("🪙 RUB", currency_data[-6]['nbu_buy_price'], currency_data[-6]['nbu_cell_price']),
                ("💴 CHF", currency_data[3]['nbu_buy_price'], currency_data[3]['nbu_cell_price']),
                ("💷 GBP", currency_data[8]['nbu_buy_price'], currency_data[8]['nbu_cell_price']),
            ]
            message_to_the_user = (f'     Exchange Rates for {structured_date}\n\n'
                                   f'{'*' * 45}\n'
                                   f'{'Currency':<25}{'Buy':<25}{'Sell':<20}\n'
                                   f'{'_' * 38}')
            for i in currencies:
                name, buy, sell = i
                if name == '🪙 RUB':
                    message_to_the_user += f'\n\n{name:<22}{buy:<22}{sell:<20}'
                else:
                    message_to_the_user += f'\n\n{name:<20}{buy:<20}{sell:<20}'

            bot.send_message(user_id, f'{message_to_the_user}\n\n'
                                      f'{'_' * 38}\n\n'
                                      f'{'*' * 45}\n\n')
            bot.register_next_step_handler(message, user_choice)

        else:
            bot.send_message(user_id, '❌ Error ❌'
                                      '\n\nPlease try again later 💬', reply_markup=buttons.start_bot_buttons())
            bot.register_next_step_handler(message, user_choice)
    elif message.text == '💸 Convert':
        bot.send_message(user_id, '⬇️ Use buttons below and convert money by NBU bank exchange rate ⬇️',
                         reply_markup=buttons.currency_convert_type())
        bot.register_next_step_handler(message, currency_convert_type)
    else:
        bot.send_message(user_id, '❌ Error ❌'
                                  '\n\n⬇️ Please use buttons below ⬇️', reply_markup=buttons.start_bot_buttons())
        bot.register_next_step_handler(message, user_choice)


def currency_convert_type(message):
    user_id = message.from_user.id
    if message.text == 'UZS >>> Any':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    elif message.text == 'ANY >>> UZS':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    elif message.text == '⬅️ Back':
        bot.send_message(user_id, '🔙Getting back',
                         reply_markup=buttons.start_bot_buttons())
        bot.register_next_step_handler(message, user_choice)
    else:
        bot.send_message(user_id, '❌ Error ❌'
                                  '\n\n⬇️ Please use buttons below ⬇️', reply_markup=buttons.start_bot_buttons())
        bot.register_next_step_handler(message, currency_convert_type)


def uzs_to_any_type(message):
    user_id = message.from_user.id
    if message.text == '💵 To USD':
        bot.send_message(user_id, 'Type in UZS (sum) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, to_USD, user_id)
    elif message.text == '💶 To EUR':
        bot.send_message(user_id, 'Type in UZS (sum) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, to_EUR, user_id)
    elif message.text == '🪙 To RUB':
        bot.send_message(user_id, 'Type in UZS (sum) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, to_RUB, user_id)
    elif message.text == '💴 To CHF':
        bot.send_message(user_id, 'Type in UZS (sum) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, to_CHF, user_id)
    elif message.text == '💷 To GBP':
        bot.send_message(user_id, 'Type in UZS (sum) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, to_GBP, user_id)
    elif message.text == '⬅️ Back':
        bot.send_message(user_id, '🔙 Getting back', reply_markup=buttons.currency_convert_type())
        bot.register_next_step_handler(message, currency_convert_type)
    else:
        bot.send_message(user_id, '❌ Error ❌'
                                  '\n\n⬇️ Please use buttons below ⬇️', reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)


def to_USD(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_USD, user_id)
            return

        try:
            uzs_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_buy_rate = float(currency_data[-1]['nbu_buy_price'])
                usd_amount = uzs_number / usd_buy_rate
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n💵 USD: $ {usd_amount:.2f}'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in UZS (sum) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, to_USD, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.uzs_to_any())
                bot.register_next_step_handler(message, uzs_to_any_type)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_USD, user_id)


def to_EUR(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_EUR, user_id)
            return

        try:
            uzs_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_buy_rate = float(currency_data[7]['nbu_buy_price'])
                eur_amount = uzs_number / usd_buy_rate
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n💶 EUR: € {eur_amount:.2f}'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in UZS (sum) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, to_EUR, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.uzs_to_any())
                bot.register_next_step_handler(message, uzs_to_any_type)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_EUR, user_id)


def to_RUB(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_RUB, user_id)
            return

        try:
            uzs_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_buy_rate = float(currency_data[-6]['nbu_buy_price'])
                rub_amount = uzs_number / usd_buy_rate
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🪙 RUB: ₽ {rub_amount:.2f}'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in UZS (sum) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, to_RUB, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.uzs_to_any())
                bot.register_next_step_handler(message, uzs_to_any_type)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_RUB, user_id)


def to_CHF(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_CHF, user_id)
            return

        try:
            uzs_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_buy_rate = float(currency_data[3]['nbu_buy_price'])
                chf_amount = uzs_number / usd_buy_rate
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n💴 CHF: ₣ {chf_amount:.2f}'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in UZS (sum) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, to_CHF, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.uzs_to_any())
                bot.register_next_step_handler(message, uzs_to_any_type)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_CHF, user_id)


def to_GBP(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to 💰',
                         reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_GBP, user_id)
            return

        try:
            uzs_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_buy_rate = float(currency_data[8]['nbu_buy_price'])
                chf_amount = uzs_number / usd_buy_rate
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n💷 GBP: £ {chf_amount:.2f}'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                 '\n\nType in UZS (sum) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, to_GBP, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.uzs_to_any())
                bot.register_next_step_handler(message, uzs_to_any_type)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, to_GBP, user_id)


def any_type_to_uzs(message):
    user_id = message.from_user.id
    if message.text == '💵 From USD':
        bot.send_message(user_id, 'Type in USD (dollar) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, from_USD, user_id)
    elif message.text == '💶 From EUR':
        bot.send_message(user_id, 'Type in EUR (euro) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, from_EUR, user_id)
    elif message.text == '🪙 From RUB':
        bot.send_message(user_id, 'Type in RUB (ruble) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, from_RUB, user_id)
    elif message.text == '💴 From CHF':
        bot.send_message(user_id, 'Type in CHF (frank) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, from_CHF, user_id)
    elif message.text == '💷 From GBP':
        bot.send_message(user_id, 'Type in GBP (pound) amount 💬', reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, from_GBP, user_id)
    elif message.text == '⬅️ Back':
        bot.send_message(user_id, '🔙 Getting back', reply_markup=buttons.currency_convert_type())
        bot.register_next_step_handler(message, currency_convert_type)
    else:
        bot.send_message(user_id, '❌ Error ❌'
                                  '\n\n⬇️ Please use buttons below ⬇️', reply_markup=buttons.uzs_to_any())
        bot.register_next_step_handler(message, uzs_to_any_type)


def from_USD(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS (sum) 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_USD, user_id)
            return

        try:
            currency_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_sell_rate = float(currency_data[-1]['nbu_cell_price'])
                uzs_amount = currency_number * usd_sell_rate
                uzs_amount = f"{uzs_amount:,.0f}".replace(',', ' ')
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🏦 UZS:  {uzs_amount} sums'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in USD (dollar) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, from_USD, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.any_to_uzs())
                bot.register_next_step_handler(message, any_type_to_uzs)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_USD, user_id)


def from_EUR(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS (sum) 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_EUR, user_id)
            return

        try:
            currency_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_sell_rate = float(currency_data[7]['nbu_cell_price'])
                uzs_amount = currency_number * usd_sell_rate
                uzs_amount = f"{uzs_amount:,.0f}".replace(',', ' ')
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🏦 UZS:  {uzs_amount} sums'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in EUR (euro) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, from_EUR, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.any_to_uzs())
                bot.register_next_step_handler(message, any_type_to_uzs)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_EUR, user_id)


def from_RUB(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS (sum) 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_RUB, user_id)
            return

        try:
            currency_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_sell_rate = float(currency_data[-6]['nbu_cell_price'])
                uzs_amount = currency_number * usd_sell_rate
                uzs_amount = f"{uzs_amount:,.0f}".replace(',', ' ')
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🏦 UZS:  {uzs_amount} sums'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in RUB (ruble) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, from_RUB, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.any_to_uzs())
                bot.register_next_step_handler(message, any_type_to_uzs)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_RUB, user_id)


def from_CHF(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS (sum) 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_CHF, user_id)
            return

        try:
            currency_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_sell_rate = float(currency_data[3]['nbu_cell_price'])
                uzs_amount = currency_number * usd_sell_rate
                uzs_amount = f"{uzs_amount:,.0f}".replace(',', ' ')
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🏦 UZS:  {uzs_amount} sums'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in CHF (frank) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, from_CHF, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.any_to_uzs())
                bot.register_next_step_handler(message, any_type_to_uzs)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_CHF, user_id)


def from_GBP(message, user_id):
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '💰 Please choose currency type to convert to UZS (sum) 💰',
                         reply_markup=buttons.any_to_uzs())
        bot.register_next_step_handler(message, any_type_to_uzs)
    else:
        user_message = message.text.strip().replace(' ', '')
        user_message = user_message.replace(',', '.')
        if user_message.count('.') > 1:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_GBP, user_id)
            return

        try:
            currency_number = float(user_message)
            url = requests.get('https://nbu.uz/uz/exchange-rates/json/')
            if url.status_code == 200:
                currency_data = url.json()
                usd_sell_rate = float(currency_data[8]['nbu_cell_price'])
                uzs_amount = currency_number * usd_sell_rate
                uzs_amount = f"{uzs_amount:,.0f}".replace(',', ' ')
                bot.send_message(user_id, f'{'*' * 45}'
                                          f'\n\n🏦 UZS:  {uzs_amount} sums'
                                          f'\n\n{'*' * 45}')
                bot.send_message(user_id, f'\n{'_' * 38}'
                                          '\n\nType in GBP (pound) amount 💬', reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, from_GBP, user_id)
            else:
                bot.send_message(user_id, '❌ Error. Could not retrieve data ❌'
                                          '\n\nPlease try again later 💬', reply_markup=buttons.any_to_uzs())
                bot.register_next_step_handler(message, any_type_to_uzs)
        except ValueError:
            bot.send_message(user_id, '❌ Error. Invalid number ❌'
                                      '\n\nPlease try again 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, from_GBP, user_id)


# Running the bot infinitely
bot.polling(non_stop=True)
