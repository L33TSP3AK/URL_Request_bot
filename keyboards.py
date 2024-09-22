from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import main, db

async def menu_kb(user_id):
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	if await main.IsAdmin().check(user_id=user_id):
		keyboard.add(KeyboardButton("💎 Admin Panel 💎"))
	keyboard.add(KeyboardButton("🔎 Search"),KeyboardButton("⏳ Available logs"))
	keyboard.add(KeyboardButton("💬 Information"),KeyboardButton("👤 Profile"))
	return keyboard

async def request_log(value):
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("💎 Request", callback_data=f"menu:reqeust_log:{value}"))
	keyboard.add(InlineKeyboardButton("👨‍💻 Contact Support", url="https://t.me/CashMoneyL33T"))
	return keyboard

async def contact_support():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("👨‍💻 Contact Support", url="https://t.me/CashMoneyL33T"))
	return keyboard

async def search_methods():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("🌐 URL", callback_data=f"menu:search:URL"))
	keyboard.add(InlineKeyboardButton("🔤 Keyword", callback_data=f"menu:search:Keyword"))
	keyboard.add(InlineKeyboardButton("👤 Username", callback_data=f"menu:search:Username"))
	keyboard.add(InlineKeyboardButton("🔑 Password", callback_data=f"menu:search:Password"))
	return keyboard

async def profile_kb():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("🎁 Activate Promocode 🎁", callback_data="menu:promocode"))
	return keyboard

async def buy_log(id):
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("💸 Buy 💸", callback_data=f"menu:buy_log:{id}"))
	return keyboard

async def admin_panel_kb():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("💎 Add Admin", callback_data="admin:add_admin"))
	keyboard.add(InlineKeyboardButton("👤 Users", callback_data="admin:users"))
	keyboard.add(InlineKeyboardButton("🎁 Create Promocode", callback_data="admin:create_promocode"))
	keyboard.add(InlineKeyboardButton("📝 Import Logs", callback_data="admin:import_logs"))
	return keyboard

async def admin_users_panel_kb():
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("👤 All Users", callback_data="admin:all_users"))
	keyboard.add(InlineKeyboardButton("🔍 Search User", callback_data="admin:search_user"))
	return keyboard

async def admin_user_panel_kb(user_id):
	keyboard = InlineKeyboardMarkup()
	ban = await db.get_datax(database="banlist",user_id=user_id)
	keyboard.add(InlineKeyboardButton("unBan" if ban else "Ban", callback_data=f"admin:ban:{user_id}"))
	return keyboard
	