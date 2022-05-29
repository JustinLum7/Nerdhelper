import logging
from pkgutil import extend_path
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(
    format='%(asctime)s - %(name)s %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

todo_list = ['To-do List:']

def start_command(update: Update, _: CallbackContext) -> None:
    user = update.message.from_user
    name = user['first_name']
    update.message.reply_text(
        f'Hi {name}!, this bot is basically a to-do list for your tasks! Commands:\n' + 
        '/addtask followed by your task to add your new task\n' + 
        '/list to view your current to-do list\n' + 
        '/donetask followed by the number of that task on the list to remove that task.\n' + 
        '/pomotime to use the pomodoro timer\n' + 
        '/endpomo to quit the timer'
    )

def help_command(update: Update, _:CallbackContext) -> None:
  update.message.reply_text('This bot is used as a to-do list, and comes with a pomodoro timer! ' + 
  'For more information on the pomodoro technique, do visit https://todoist.com/productivity-methods/pomodoro-technique \n' + 
  'For a list of the commands, press /start')

def show_list(update: Update, _:CallbackContext) -> None:
  str = f'{todo_list[0]}\n'
  for i in range (1, len(todo_list)):
    str += f'{i}. ' + f'{todo_list[i]}\n'
  update.message.reply_text(f'{str}')

def add_task(update: Update, _:CallbackContext) -> None:
  text = update.message.text
  task_arr = text.split(' ')[1:]
  task_str = ''
  for i in range (len(task_arr)):
    task_str += f'{task_arr[i]} '
  todo_list.append(f'{task_str}')
  str = ''
  str = f'{todo_list[0]}\n'
  for i in range (1, len(todo_list)):
    str += f'{i}. ' + f'{todo_list[i]}\n'
  update.message.reply_text(f'{str}')

def done_task(update: Update, _:CallbackContext) -> None:
  text = update.message.text
  numbers = text.split(' ')[1:]
  number = int(numbers[0])
  todo_list.pop(number)
  str = f'{todo_list[0]}\n'
  for i in range (1, len(todo_list)):
    str += f'{i}. ' + f'{todo_list[i]}\n'
  update.message.reply_text(f'{str}')

def create_new(update: Update, _:CallbackContext) -> None:
  todo_list = ['To-do List:']
  update.message.reply_text(f'{todo_list[0]}')

def main() -> None:
  token = '5362228092:AAHZs65AIhRe9osKuQPPQRuSzCAsjBdjcD8'

  updater = Updater(token)

  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler('start', start_command))
  dispatcher.add_handler(CommandHandler('help', help_command))
  dispatcher.add_handler(CommandHandler('list', show_list))
  dispatcher.add_handler(CommandHandler('addtask', add_task))
  dispatcher.add_handler(CommandHandler('donetask', done_task))
  dispatcher.add_handler(CommandHandler('newlist', create_new))


  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()

