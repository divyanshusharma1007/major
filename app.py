from aiohttp import web 

from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton

import telebot


token = "6417872030:AAG352xW0_9oyEngmdvV8pZ3GDo92kA319w"
bot1 = Bot(token)
Bot.set_current(bot1)

dispatcher = Dispatcher(bot1)

app=web.Application()

webhook_path = f'/{token}'

async def set_webhook():
    webhook_uri = f'https://sweeping-peacock-locally.ngrok-free.app{webhook_path}'
    await bot1.set_webhook(
        webhook_uri
    )
    
async def on_startup(_):
    await set_webhook()

    
bot = telebot.TeleBot(token)

@dispatcher.message_handler(commands = ['start'])
async def fun(message:types.Message):
    print(message)
    await bot1.send_message(message.chat.id,"let's start")

@dispatcher.message_handler(commands = ['about'])
async def about(message:types.Message):
    print(message)
    await bot1.send_message(message.chat.id,"this bot is developed by divyanshu sharma")
    
@dispatcher.message_handler(content_types=[
    types.ContentType.PHOTO,
    types.ContentType.DOCUMENT,
    types.ContentType.AUDIO,
    types.ContentType.VIDEO,
    types.ContentType.VOICE,
    types.ContentType.STICKER,
    types.ContentType.LOCATION,
    types.ContentType.CONTACT,
    types.ContentType.POLL,
])
async def on_other_message(message: types.Message):
    await message.answer("Sorry, I cannot process images, files, or other types of content. i am sepecially designed to answer the tax related queries")

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    print("running")
    if token == token:
        update = types.Update(**await request.json())
        await dispatcher.process_update(update)
        
        return web.Response()
    else:
        return web.Response(status=403)






app.router.add_post(f'/{token}', handler=handle_webhook)

if __name__ == "__main__":
    app.on_startup.append(on_startup)
    
    web.run_app(
        app,
        host='0.0.0.0',
        port='5000'
    )