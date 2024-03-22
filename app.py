from aiohttp import web
from aiogram import Bot, Dispatcher, types
from openai import ChatCompletion
import openai

TOKEN = "6417872030:AAG352xW0_9oyEngmdvV8pZ3GDo92kA319w"  # Replace with your bot token
API_KEY = "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"  # Replace with your OpenAI API key

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
chatgpt = ChatCompletion(api_key=API_KEY)

async def set_webhook():
    webhook_uri = f"https://74a2-2409-4081-9e18-b507-c83-70f-ee1e-82d6.ngrok-free.app/{TOKEN}"
    try:
        await bot.set_webhook(webhook_uri)
        Bot.set_current(bot)
    except Exception as e:
        print(f"Error setting webhook: {e}")

async def on_startup(_):
    await set_webhook()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer('''
👋 Welcome to the Taxation-Bot , we are here to help you 
We're here to make your journey through the complex world of Indian taxation as smooth and straightforward as possible. Whether you're an individual taxpayer or a business owner, our cutting-edge bot is designed to provide you with accurate, real-time, and personalized tax-related solutions.
''')

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
    await message.answer('''
Name: Taxation Bot
Username: @Indian_taxation_bot
Version: 1.1.1
📜 Description:
The Generative Telegram Bot for Indian Taxation simplifies tax complexities in India. 🇮🇳 It offers real-time updates, personalized assistance, and educational resources, enhancing financial literacy and promoting tax compliance. 📊💰 It prioritizes user data security and privacy. 🔒

👥 Developers:

Divyanshu Sharma 🚀

Email: 1007divyanshu@gmail.com
Hemshika Nayak 📊

Kapil Sahu 🔐

Keshavi Dubey 💡

This team of developers has worked tirelessly to create a bot that makes dealing with Indian taxation easier and more secure for users. 🙌

''')

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def on_message_received(message: types.Message):
    tax_related = any(keyword in message.text.lower() for keyword in ['tax', 'taxes', 'taxable', 'deduction', 'income tax', 'sales tax','gst'])
    if tax_related:
        response = await generate_chatgpt_response(message.text)
        await message.answer(response)
    else:
        await message.answer("This bot is specially designed to assist with tax-related queries.")
openai.api_key =API_KEY

async def generate_chatgpt_response(prompt):
    try:
        response = await openai.Completion.create(
            engine="gpt-3.5-turbo-16k-0613",  # Improved model choice based on task
            prompt=f"**system:** {prompt}",
            max_tokens=1024,  # Adjust max response length as needed
            n=1,
            stop=None,  # Optional stop sequence
            temperature=0.7,  # Control creativity vs. informativeness
        )
        
        if response.choices:
            return response.choices[0].text.strip()
        else:
            return "I couldn't generate a response for that."
    except Exception as e:
        print(f"Error generating ChatGPT response: {e}")
        return "I encountered an error while generating a response."
    
async def handle_webhook(request):
    if request.method == 'POST':
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=405)

app = web.Application()
app.router.add_post(f'/{TOKEN}', handle_webhook)
app.router.add_get("/", handle_webhook)

if __name__ == "__main__":
   
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=5000)