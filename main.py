"""
░█▀▀█ █▀▀█ █▀▀ █──█ ░█▀▄▀█ █▀▀█ █▀▀▄ █▀▀ █──█ ░█─── █▀▀█ █▀▀█ ▀▀█▀▀ 
░█─── █▄▄█ ▀▀█ █▀▀█ ░█░█░█ █──█ █──█ █▀▀ █▄▄█ ░█─── ──▀▄ ──▀▄ ─░█── 
░█▄▄█ ▀──▀ ▀▀▀ ▀──▀ ░█──░█ ▀▀▀▀ ▀──▀ ▀▀▀ ▄▄▄█ ░█▄▄█ █▄▄█ █▄▄█ ─░█──

                                                
CashMoneyL33T - - A Underground Mentor & Entrapenur 
Version: 1.3.3.7
Created by: CashMoneyL33T
GitHub: https://github.com/L33TSP3AK
Telegram: https://t.me/CashMoneyL33T
License: MIT

"Scripts, Logs, Configs, Projects & More Available"

"""

from aiogram import Bot, types,executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command 
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils.exceptions import MessageNotModified, RetryAfter
from aiogram.contrib.fsm_storage.memory import MemoryStorage  
from aiogram.dispatcher.filters.state import StatesGroup, State 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import logging, asyncio, os, random
from time import strftime

import db, keyboards

bot_token = "000000000000000:fbdzdfzbzdfbzdbzdfbdzfbdfbdbhr"
chat_admins = 0000000000
price_one_log = 1

storage = MemoryStorage()
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
dp = Dispatcher(bot,storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',level=logging.INFO,)

async def print_name(name):
    name = name.replace("<", "&lt;").replace(">", "&gt;")
    return name

async def add_log(message,text):
    user_text = f'''<a href='tg://user?id={message.from_user.id}'>{await print_name(message.from_user.full_name)}</a>'''
    send_text = f'{user_text} | {text}\n\n🆔 <code>{message.from_user.id}</code> 🧸 {message.from_user.get_mention()}' 
    await bot.send_message(chat_id=chat_admins, text=send_text) 

class IsAdmin(BoundFilter):
	async def check(self, user_id):
		try:
			state = await db.get_datax(database="admins",user_id=user_id)
			if state:
				return True
			else:
				return False
		except:
			return False
          
class IsBanned(BoundFilter):
	async def check(self, message):
		try:
			state = await db.get_datax(database="banlist",user_id=message.from_user.id)
			if state:
				return True
			else:
				return False
		except:
			return False

@dp.message_handler(IsBanned())
async def is_banned(message: types.message):
    if await db.check_user(message.from_user.id) == False:
        await add_log(message, f"😍 Now registered in the bot!")
        await db.add_database(message)
    ban = await db.get_datax(database="banlist",user_id=message.from_user.id)
    await message.answer(f'''
😔 Unfortunately you are banned!

{f"🚫 Reason: {ban['ban_reason']}" if ban['ban_reason'] else ""}
''', reply_markup=await keyboards.contact_support())

@dp.message_handler(Command("start"), state=None,chat_type=types.ChatType.PRIVATE)
async def welcome(message: types.Message):
    if await db.check_user(message.from_user.id) == False:
        await add_log(message, f"😍 Now registered in the bot!")
    await db.add_database(message)
    await message.answer(f"😉 Hello {message.from_user.get_mention()}!", reply_markup=await keyboards.menu_kb(message.from_user.id))

@dp.message_handler(content_types=['text'], chat_type=types.ChatType.PRIVATE)
async def get_message(message: types.message):
    if "🔎 Search" == message.text:
        await message.answer(f'''
<i>{message.text}</i>
                                                
💫 Please select search function:''', reply_markup=await keyboards.search_methods())
    elif "👤 Profile" == message.text:
        get_user = await db.get_datax(database="users", user_id=message.from_user.id)
        purchases = await db.get_datax(database="purchases", user_id=message.from_user.id, all=True)
        await message.answer(f'''
<i>{message.text}</i>

🆔: <code>{message.from_user.id}</code>

💸 Balance: <code>{get_user['balance']}</code> $
💫 Purchased logs: <code>{len(purchases)}</code>
''', reply_markup=await keyboards.profile_kb())
    elif "💬 Information" == message.text:
        users = await db.get_datax(database="users", all=True,not_where=True)
        logs = await db.get_datax(database="logs", not_where=True, all=True)
        purchases = await db.get_datax(database="purchases", not_where=True, all=True)
        await message.answer(f'''
<i>{message.text}</i>

👤 Users: <code>{len(users)}</code>
📝 Current Logs: <code>{len(logs)}</code>
⏳ Submitted Logs: <code>{len(logs) + len(purchases)}</code>
💫 Purchases: <code>{len(purchases)}</code>
''', reply_markup=await keyboards.contact_support())
    elif "⏳ Available logs" == message.text:
        logs = await db.get_datax(database="logs", not_where=True, all=True)
        website_counts = {}
        for log in logs:
            website = log['website']
            website_counts[website] = website_counts.get(website, 0) + 1
        
        output_string = "\n".join([f"{website} - <code>{count}</code>" for website, count in website_counts.items()])
        await message.answer(f'''
<i>{message.text}</i>

{output_string}
''')
    elif "💎 Admin Panel 💎" == message.text:
        if await IsAdmin().check(user_id=message.from_user.id):
            await message.answer('Admin Panel', reply_markup=await keyboards.admin_panel_kb())

@dp.callback_query_handler(text_startswith="menu")
async def menu_callback(call: types.CallbackQuery, state: FSMContext):
    variant = call.data.split(":")[1]
    get_user = await db.get_datax(database="users", user_id=call.from_user.id)
    if variant == "search":
        type = call.data.split(":")[2]
        await call.message.edit_text(f'📝 Write {type}:')
        await state.update_data(type=type)
        await Main.Search.set()
    elif variant == "reqeust_log":
        request = call.data.split(":")[2]
        await add_log(call, f"❗️ Request log: <code>{request}</code>")
        await call.message.edit_text(f'✅ Send Request log <code>{request}</code>!')
    elif variant == "promocode":
        await call.message.edit_text('✏️ Write promocode:')
        await Main.ActivatePromocode.set()
    elif variant == "buy_log":
        id = call.data.split(":")[2]
        log = await db.get_datax(database="logs", id=id)
        print(log)
        if int(get_user['balance']) >= int(price_one_log):
            if log:
                
                data = f"{log['website']}:{log['login']}:{log['password']}"

                await db.update_datax(update_parameters={
                    "balance": f"{int(get_user['balance']) - int(price_one_log)}"
                }, where_parameters={
                    "user_id": call.from_user.id
                })
                await db.drop_column(table="logs", id=id, login=log['login'], password=log['password'])
                await db.add_purchases(call.from_user.id, data, price_one_log)
                await call.message.edit_text(f'''
✅ Purchased log!
                                        
🌐 Website: {log['website']}
👤 Login: <code>{log['login']}</code>
🔑 Password: <code>{log['password']}</code>
''')
            else:
                await call.message.edit_text('😔 Not found log', reply_markup=await keyboards.contact_support())
        else:
            await call.answer('😔 There is not enough money to buy', show_alert=True)


@dp.callback_query_handler(text_startswith="admin")
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    variant = call.data.split(":")[1]
    if variant == "add_admin":
        await call.message.edit_text("Please write ID new admin:")
        await Main.AddAdmin.set()
    elif variant == "create_promocode":
        await call.message.edit_text("Please write amount promocode:")
        await Main.CreatePromocode.set()
    elif variant == "import_logs":
        await call.message.edit_text("Please send me .txt file. Format to .txt file: website<code>:</code>login<code>:</code>password")
        await Main.ImportLogs.set()
    elif variant == "users":
        users = await db.get_datax(database="users", all=True,not_where=True)
        await call.message.edit_text(f"Users: {len(users)}", reply_markup=await keyboards.admin_users_panel_kb())
    elif variant == "search_user":
        await call.message.edit_text("Please write Telegram ID user:")
        await Main.SearchUser.set()
    elif variant == "all_users":
        await call.message.answer("Loading...")
        users = await db.get_datax(database="users", all=True,not_where=True)
        text = ""
        for user in users:
            text += f'''🆔 ID: {user['user_id']}\n💸 Balance: {user['balance']}$\n🕐 DateReg: {user['date']}\n\n'''
        try:
            if len(text) > 4096:
                for x in range(0, len(text), 4096):
                    await call.message.answer(text[x:x+4096])
            else:
                await call.message.answer(text)
        except Exception as err:
            print(err)
            await call.message.answer(f'❌ Error: {err}')
    elif variant == "ban":
        user_id = call.data.split(":")[2]
        ban = await db.get_datax(database="banlist",user_id=user_id)
        if ban:
            await db.drop_column(table="banlist", user_id=user_id)
            await call.answer("✅ unBanned",show_alert=True)
        else:
            await db.add_ban(user_id)
            await call.answer("✅ Banned",show_alert=True)


async def process_search_results(message, logs, text):
    if logs:
        get_user = await db.get_datax(database="users", user_id=message.from_user.id)
        log = random.choice(logs)
        await message.answer(f'''
🔍 Found: <code>{len(logs)}</code> logs
💸 Balance: <code>{get_user['balance']}</code> $
1️⃣ Log price: <code>{price_one_log}</code> $
''', reply_markup=await keyboards.buy_log(log['id']))
    else:
        await message.answer("😔 Nothing was found for this query!", reply_markup=await keyboards.request_log(text))

class Main(StatesGroup):
    ActivatePromocode = State()
    Search = State()
    # Admin
    AddAdmin = State()
    ImportLogs = State()
    SearchUser = State()
    CreatePromocode = State()


@dp.message_handler(state=Main.Search)
async def search(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    if data['type'] == "URL":
        url = text.replace('https://', '').replace('http://', '').replace('/', '')
        logs = await db.get_datax(database="logs", website=url, all=True)
    elif data['type'] == "Keyword":
        logs = await db.get_datax_like(database="logs", column="website", value=text, all=True)
    elif data['type'] == "Username":
        logs = await db.get_datax(database="logs", login=text, all=True)
    elif data['type'] == "Password":
        logs = await db.get_datax(database="logs", password=text, all=True)
    await process_search_results(message, logs, text)
    await state.finish()

@dp.message_handler(state=Main.AddAdmin)
async def AddAdminSG(message: types.Message, state: FSMContext):
    user_id = message.text
    await db.add_admin(user_id)
    await message.answer(f"Success")
    await state.finish()

@dp.message_handler(state=Main.ImportLogs, content_types=["document", "text"])
async def ImportLogsSG(message: types.Message, state: FSMContext):
    if message.text:
        await message.answer('No .txt file!')
        await state.finish()
    elif message.document:
        document = message.document
        if document.mime_type == 'text/plain' and document.file_name.endswith('.txt'):
            await message.answer("Read file...")

            file_path = f'import_logs/{strftime("%Y-%m-%d_%H-%M-%S")}_{document.file_name}'
            file = await bot.get_file(document.file_id)
            await bot.download_file(file.file_path, file_path)
            print(file_path)
            ok, err = 0, 0
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    try:
                        line = line.replace('https://', '').replace('http://', '').replace('/', '')
                        website = line.split(':')[0]
                        login = line.split(':')[1]
                        password = line.split(':')[2]
                        await db.add_logs(website, login, password)
                        ok += 1
                    except:
                        err += 1
            await message.answer(f"Success import\n✅: {ok}\n❌: {err}")
            os.remove(file_path)
        else:
            await message.answer("Pls send .txt file!")
    else:
        await message.answer("Not found file!")
    await state.finish()  

@dp.message_handler(state=Main.SearchUser)
async def SearchUserSG(message: types.Message, state: FSMContext):
    user_id = message.text
    if user_id.isdigit():
        get_user = await db.get_datax(database="users", user_id=user_id)
        ban = await db.get_datax(database="banlist", user_id=user_id)
        if get_user:
            user_info = await bot.get_chat(user_id)
            purchases = await db.get_datax(database="purchases", user_id=message.from_user.id, all=True)
            await message.answer(f'''
🔎 View Profile {user_info.get_mention()}

👤 Name: {await print_name(user_info.full_name)}
🆔 ID: <code>{get_user['user_id']}</code>
#️⃣ UserName: @{user_info.username}
🚫 Ban: {f"Yes | <code>{ban['date']}</code>" if ban else "No"}


💸 Balance: <code>{get_user['balance']}</code> $
💫 Purchased logs: <code>{len(purchases)}</code>
🕐 DateReg: <code>{get_user['date']}</code>
''', reply_markup=await keyboards.admin_user_panel_kb(user_id))
        else:
            await message.answer(f'''
🔎 User <code>{user_id}</code> not found!

🆔 ID: <code>{user_id}</code>
🚫 Ban: {f"Yes | <code>{ban['date']}</code>" if ban else "No"}
''', reply_markup=await keyboards.admin_user_panel_kb(user_id))
    else:
        await message.answer('No int message')
    await state.finish()

@dp.message_handler(state=Main.ActivatePromocode)
async def ActivatePromocodeSG(message: types.Message, state: FSMContext):
    name = message.text
    promocode = await db.get_datax(database="promocodes", name=name)
    if promocode:
        await db.drop_column(table="promocodes", name=name)
        get_user = await db.get_datax(database="users", user_id=message.from_user.id)
        await db.update_datax(update_parameters={
            "balance": f"{int(get_user['balance'])+int(promocode['amount'])}"
        }, where_parameters={
            "user_id": message.from_user.id
        })
        await message.answer(f'✅ Activated promocode, give <code>{promocode["amount"]}</code>$')
    else:
        await message.answer('❗️ Not found promocode')
    await state.finish()

@dp.message_handler(state=Main.CreatePromocode)
async def CreatePromocodeSG(message: types.Message, state: FSMContext):
    amount = message.text
    if amount.isdigit():
        сharacters = "abcdefghijklmnopqrstuvwxyz1234567890"
        name = ''.join(random.choice(сharacters) for _ in range(random.randint(8, 16)))
        await db.add_promo(name, amount)
        await message.answer(f"💫 Created promocode:\n\n📝 Name: <code>{name}</code>\n💰 Amount: <code>{amount}</code>$")
    else:
        await message.answer('No int message')
    await state.finish()
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.create_tables())
    executor.start_polling(dp, skip_updates=False)