import telebot
import requests
from bs4 import BeautifulSoup
import time

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
token = '6540041877:AAGz1D77-mHyJ3MlmmZizlqbGGDv-sNKYNM'
bot = telebot.TeleBot(token)

# Telegram Chat ID
CHAT_ID = '-1001833864444'  # Replace with your group chat ID

def telegram_bot_sendtext(bot_message):
    send_text = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': bot_message, 'parse_mode': 'Markdown'}
    response = requests.get(send_text, params=params)

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Message sending failed. Status code: {response.status_code}")

# Initialize a variable to store the last sent value
last_sent_value = None

@bot.message_handler(commands=['start', 'stop'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Bot is started")
        # Start scraping and sending messages
        while True:
            check_item()
    elif message.text == '/stop':
        bot.send_message(message.chat.id, "Bot is stopped")
    else:
        # Print the user's message to the console
        print(f"User ID {message.from_user.id}: {message.text}")

def check_item():
    global last_sent_value

    url = 'https://eubank.kz'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the span element based on the provided attributes
    target_span_sale = soup.find('span', {'data-type': '2', 'data-code': 'USD', 'data-direction': 'sale'})
    target_span_buy = soup.find('span', {'data-type': '1', 'data-code': 'USD', 'data-direction': 'buy'})

    # Extract the text content within the span element
    if target_span_buy and target_span_sale:
        span_text_sale = target_span_sale.text.strip()
        span_text_buy = target_span_buy.text.strip()

        # Compare with the last sent value
        if span_text_sale != last_sent_value:
            # Send a message and update the last sent value
            message = f"Покупка: ${span_text_buy}\nПродажа: ${span_text_sale}"
            telegram_bot_sendtext(message)
            last_sent_value = span_text_sale
    else:
        print("Span element not found.")
        telegram_bot_sendtext("Ошибка! Проверьте сайт https://eubank.kz")

    # Sleep for a while before checking again (e.g., every 2 minutes)
    time.sleep(120)

if __name__ == '__main__':
    bot.polling()
