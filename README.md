# 🔐 Telegram Log Management & Search Bot 🔍

This Python project leverages the power of `aiogram` to create a Telegram bot that facilitates efficient log management and searching. With features for both users and admins, it provides a comprehensive solution for handling log data and user interactions.

## ✨ Core Features ✨

### 📂 Log Management

* **🔍 Searching:** Users can search for logs based on various criteria, including:
    * 🔗 URL
    * 🔑 Keyword
    * 👤 Username
    * 🔑 Password
* **💰 Balance & Purchase:** Search results showcase:
    * 🔢 The number of matching logs
    * 💲 The user's current balance
    * 💸 The option to purchase individual logs
    * 📝 The ability to request new logs if none are found
* **📤 Import:** Admins have the capability to import logs in bulk from a `.txt` file (following the format: `website:login:password`)


![image](https://github.com/user-attachments/assets/96f86f15-a81c-43fe-a193-22335008da95)

### 👮 Admin Panel

* **🎛️ Comprehensive Controls:** The admin panel offers a range of functions:
    * ➕ Add new admins by their Telegram ID
    * 🎫 Create promo codes with custom amounts
    * 👥 View all users or search for a specific user by Telegram ID
    * 🚫 Ban or unban users
    * ℹ️ View detailed user information, including:
        * 💲 Balance
        * 📂 Purchased logs
        * 📅 Registration date

### 👤 User Management

* **💾 Database Storage:** User information, including balance and purchase history, is securely stored in a database
* **🕵️‍♀️ Admin Oversight:** Admins can view user details and have the power to manage bans

## ⚙️ Technical Overview ⚙️

* **🐍 Dependencies:**
    * `aiogram`
    * A database library (e.g., `asyncpg`) for persistent data storage
* **🔄 States:**
    * Multiple `StatesGroup` are utilized to manage the flow of user interactions, covering actions like searching, adding admins, importing logs, and more
* **🤖 Message Handlers:**
    * The code defines various message handlers to effectively respond to user commands and actions within different states
* **🗃️ Database Interactions:**
    * Functions like `db.get_datax`, `db.add_logs`, and `db.add_admin` handle database operations for seamless data storage and retrieval

## 🚀 Installation & Setup 🚀

1.  Clone the repository: `git clone <repository_url>`
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Configure the database connection and provide your Telegram bot token in the settings
4. Run the bot and start managing your logs!


## 🚀 Powered by CashMoneyL33T 🚀

🔗 Connect on Telegram: [@CashMoneyL33T](https://t.me/CashMoneyL33T)

🤝 Your contributions fuel the innovation! Got ideas or want custom scripts? Hit me up!

☕ Feeling generous? Fuel the coding sessions with a caffeine boost!

| Cryptocurrency | Network/Blockchain | Wallet Address                                |
|---|---|---|
| USDT (ERC20)  | Ethereum          | `0xC6AC9f96f5365005fc0515c61CA7Bc31612De598` |
| USDT (TRC20)  | Tron              | `TNzb4anVHyTX8hVDkRirBkMYGGvypJi23D`     |
| Bitcoin (BTC) | Bitcoin           | `32WjJxt7bgaJkDRLN79P7hhivtVp9XqZqa`     |
| Ether (ETH)    | Ethereum          | `0xC5602B7F93dA2EE66D676195fc4EC3aA30fe369f` |
| Litecoin (LTC) | Litecoin           | `MPi4tRH9PDfbSqabS2i4RZyZieHZVer4Xt`     |
| Tron (TRX)     | Tron              | `THAvPAwSzNubqajqwHovBwvHBgAk5BfDWx`     |
