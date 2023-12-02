from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import json

TELEGRAM_BOT_TOKEN = "6782080124:AAES8xDqcDBL-Xm2xWmKfJEMa9YLt6mNvIQ" # СЮДИ СВІЙ ТОКЕН
WALLET_ADDRESS = ["russianbybit", "mexcrussiand", "mexcdeposit1", "russianhuobi", "huobirussian", "bybitrussian"] #СЮДИ СПИСОК КОШЕЛІВ
last_received_action = {"russianbybit": 0, "mexcrussiand": 0, "mexcdeposit1": 0,"russianhuobi": 0,"huobirussian": 0,"bybitrussian": 0,}


msg_chat_id = ['5622691128', '-1002139718697'] #СЮДИ СПИСОК ЮЗЕРІВ НА ВІДСТУК
def send_notification(context: CallbackContext):
      update: Update = context.job.context
      bot: Bot = context.bot

      for address in WALLET_ADDRESS:
          node_url = f"https://wax.blokcrafters.io/v2/history/get_actions?account={address}&skip=0&limit=100&sort=desc&transfer.to={address}"
          receive_info = requests.get(node_url).json()
          received_action = receive_info['actions'][0]['act']
          #received_from = received_action['data']['from']
          received_amount = received_action['data']['amount']
          received_time = receive_info['actions'][0]['timestamp']
          received_memo = received_action['data']['memo']

          if received_action != last_received_action[address]:
              last_received_action[address] = received_action
              message = f"Отримано💸: *{received_amount}*\nWAXP на гаманець💳:  *{address}*\nMemo:  *{received_memo}*\nЧас⏰:  *{received_time}*"
              for chid in msg_chat_id:
                  bot.send_message(chat_id=chid, text=message, parse_mode= 'Markdown')
          else:
              print(f"There are no new transactions on wallet {address}")



def start(update: Update, context: CallbackContext) -> None:
      update.message.reply_text('Я персональний бот Velonce для відслідковування транзакцій на їх гаманцях!')

def main():
      updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

      dp = updater.dispatcher

      dp.add_handler(CommandHandler("start", start))

      dp.job_queue.run_repeating(send_notification, interval=60, first=0, context=None)

      updater.start_polling()
      updater.idle()

if __name__ == '__main__':
  main()