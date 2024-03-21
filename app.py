from aiohttp import web
from aiogram import Bot, Dispatcher, types
from openai import ChatCompletion  # Import openai module
import re

async def validate_tax_string(input_string):
    tax_pattern = r'\b(tax|taxes|taxable|deduction|income tax|sales tax)\b'
    return bool(re.search(tax_pattern, input_string, re.IGNORECASE))

async def generate_chatgpt_response(message):
    api_key = "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"
    chatgpt = ChatCompletion(api_key=api_key)
    response = chatgpt.complete(prompt=message, max_tokens=50)
    return response.choices[0].text.strip()

TOKEN = "6417872030:AAG352xW0_9oyEngmdvV8pZ3GDo92kA319w"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def set_webhook():
    webhook_uri = "https://example.com/your_webhook_path"  # Update with your webhook URL
    await bot.set_webhook(webhook_uri)

async def on_startup(_):
    await set_webhook()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Let's start")

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer("This bot is developed by Divyanshu Sharma")

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def on_message_received(message: types.Message):
    if await validate_tax_string(message.text):
        await message.answer("This bot is developed by Divyanshu Sharma")
    else:
        response = await generate_chatgpt_response(message.text)
        await message.answer(response)

@dp.message_handler(content_types=[
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
    await message.answer("Sorry, I cannot process images, files, or other types of content. I am specially designed to answer tax-related queries.")

async def handle_webhook(request):
    url = str(request.url)
    token_index = url.rfind('/')
    token = url[token_index + 1:]
    if token == TOKEN:
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)

app = web.Application()
app.router.add_post(f'/{TOKEN}', handle_webhook)
app.router.add_get("/", handle_webhook)

if __name__ == "__main__":
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=5000)
