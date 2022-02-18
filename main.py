import json
import asyncio
import logging

from telethon.sync import TelegramClient
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, ChatType
from telethon.errors import ChannelPrivateError
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import funcs
import config
import keyboards
from bot_states import SetMessage, SetDelay

# Setting global groups variable
groups = []

# Setting logger
log_format = '%(levelname)s: %(asctime)s: %(message)s '
logging.basicConfig(filename='bot.log', level='INFO', format=log_format)
logger = logging.getLogger()

# Initialize bot and dispatcher
API_TOKEN = config.bot_token
bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

# Connecting a client(userbot)
client = TelegramClient(config.phone_number, config.api_id, config.api_hash)
client.connect()

# Check if a client authorized, if not sending code request to its telegram
if not client.is_user_authorized():
    client.send_code_request(config.phone_number)
    client.sign_in(config.phone_number, input('Enter the code: '))


@dp.message_handler(chat_type=[ChatType.CHANNEL, ChatType.SUPERGROUP, ChatType.GROUP])
async def ignore_groups(message: types.Message, ):
    # Ignore non-Private chats
    pass


@dp.message_handler(lambda message: message.from_user.username not in config.usernames)
async def access(message: types.Message):
    # Ignore non-admins
    pass


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='/exit', ignore_case=True), state='*')
async def get_cancelled(message: types.Message, state: FSMContext):
    # Cancel awaiting response

    await state.finish()
    await message.reply('Cancelled ✔️', reply=False, reply_markup=keyboards.main_keyboard())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    # Greetings a user

    to_print = 'Hello, I\'m here to help you to manage sending messages to groups'
    await message.reply(to_print, reply_markup=keyboards.main_keyboard(), reply=False)


@dp.message_handler(regexp=keyboards.delay_btn)
async def delay_handler(message: types.Message):
    # Asking a user to put new delay

    delay = funcs.get_delay()

    await SetDelay.delay.set()
    to_print = f"Now you have delay of <b>{delay}</b> seconds, if you want to change it just send me new delay." \
               f"<code>\n\nIf case you want to cancel changing delays press</code> /cancel"
    await message.reply(to_print)


@dp.message_handler(state=SetDelay.delay, content_types=ContentType.TEXT)
async def delay_handler_finish(message: types.Message, state: FSMContext):
    # Handling and setting new delay given by a user

    delay = message.text
    await state.finish()

    if delay.isdigit():
        funcs.set_delay(delay)
        await message.reply(f"The delay has been updated to <b>{delay}</b> second(s) ✅")
    else:
        await message.reply(f"Only digits accepted ⚠️")


@dp.message_handler(regexp=keyboards.message_btn)
async def message_handler(message: types.Message):
    # Asking a user to put new delay

    await SetMessage.message.set()
    to_print = 'Enter your message down bellow' \
               '\n\n<code>If you wan to cancel changing the message just press </code> /cancel'
    await message.reply(to_print, reply=False, reply_markup=keyboards.ReplyKeyboardRemove())


@dp.message_handler(state=SetMessage.message, content_types=ContentType.TEXT)
async def message_handler_finish(message: types.Message, state: FSMContext):
    # Handling and setting new message given by a user

    await state.finish()
    funcs.set_message(message.parse_entities())

    await message.reply('The message has been updated ✅', reply=False)
    await message.reply(message.parse_entities(), reply=False, reply_markup=keyboards.main_keyboard())


@dp.message_handler(regexp=keyboards.groups_btn)
async def group_handler(message: types.Message):
    # Return list of marked user's groups as inline keyboard

    global groups
    groups = await funcs.get_groups(client)
    parsed_groups = funcs.parse_groups(groups)

    to_print = "Pick up groups by pressing on them"
    await message.reply(to_print, reply_markup=keyboards.inline_keyboard(parsed_groups))


@dp.callback_query_handler(lambda query: query.data == 'home')
async def home_query(query: types.CallbackQuery):
    # Remove inline keyboard with user's groups

    await query.answer('🏠 Home')
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text='Returned Home 🏠')


@dp.callback_query_handler()
async def groups_queries(query: types.CallbackQuery):
    # Handle call back queries of a user editing settings

    await query.answer('Done')
    counter = int(query.data.replace('set', ''))

    global groups
    funcs.change_settings(groups[counter][0])
    parsed_groups = funcs.parse_groups(groups)

    to_print = "Pick up groups by pressing on them"
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=to_print,
                                reply_markup=keyboards.inline_keyboard(parsed_groups))


async def send_message():
    # Sending saved messages to a list of given groups

    while True:
        groups_saved = json.load(open('groups.json', 'r'))
        delay, message = json.load(open('db.json', 'r')).values()
        if groups_saved:  # Check if groups list is not empty
            for group in groups_saved:
                groups_saved_checker = json.load(open('groups.json', 'r'))

                if group in groups_saved_checker and delay and message:  # Double check if data is given
                    try:
                        await client.send_message(group, message, parse_mode='html')
                    except ChannelPrivateError:
                        funcs.delete_left_group(group)
                    except Exception:
                        logger.exception(f"Couldn't send message to {group}")
                    await asyncio.sleep(int(1))
                else:
                    await asyncio.sleep(20)
        else:
            await asyncio.sleep(20)
        await asyncio.sleep(int(delay))


if __name__ == '__main__':
    asyncio.get_event_loop().create_task(send_message())
    executor.start_polling(dp, skip_updates=True)
