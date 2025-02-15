# NBU Exchange Rates Bot 🏦

A **Python-based Telegram bot** that provides real-time exchange rates and currency conversion from the National Bank of Uzbekistan (NBU). Users can check current exchange rates and convert between UZS (Uzbek Sum) and various major currencies. Built using the **PyTelegramBotAPI** library, this bot is a comprehensive currency conversion tool.

---

## Features

### Exchange Rates
- **Current Rates**: Get real-time NBU exchange rates
- **Multiple Currencies**: Supports USD, EUR, RUB, CHF, and GBP
- **Buy/Sell Rates**: Shows both buying and selling rates
- **Formatted Display**: Clean presentation with currency symbols

### Currency Conversion
- **UZS to Foreign Currency**: Convert from Uzbek Sum to other currencies
- **Foreign Currency to UZS**: Convert from other currencies to Uzbek Sum
- **Real-time Rates**: Uses current NBU rates for accurate conversion
- **Number Format**: Supports both decimal point and comma formats

### User Interface
- **Interactive Buttons**: Easy navigation through button menus
- **Step-by-step Process**: Guided currency conversion
- **Error Handling**: Clear error messages and input validation
- **Back Navigation**: Easy return to previous menus

### Supported Currencies
- 💵 USD (US Dollar)
- 💶 EUR (Euro)
- 🪙 RUB (Russian Ruble)
- 💴 CHF (Swiss Franc)
- 💷 GBP (British Pound)

---

## Requirements

- Python 3.x
- PyTelegramBotAPI
- Requests (for API calls)
- python-dotenv (for environment variable management)
- NBU Exchange Rates API access

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GhostKX/NBU-Bank-Currency-Rates-bot.git
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot

- Create a .env file to store your Telegram API Key and OpenWeatherMap API Key
- Add your Telegram Bot Token:

```
API_KEY=your-telegram-bot-token
```

4. Navigate to the project directory
```bash
cd NBU-Bank-Currency-Rates-bot
```

5. Run the bot
```bash
python PythonNBUBankAllCurrencies_bot.py
```

## Usage

### Initial Setup
1. Start the bot with `/start`
2. Choose an option:
   - **📈 Exchange rates**: View current NBU rates
   - **💸 Convert**: Convert between currencies


### Exchange Rate Check
- Select "📈 Exchange rates" to view current rates for all supported currencies
- Rates are displayed in a formatted table showing:
  - Currency name and symbol
  - Buy rate
  - Sell rate


### Currency Conversion
1. Select "💸 Convert"
2. Choose conversion direction:
   - **UZS >>> Any**: Convert from Uzbek Sum
   - **ANY >>> UZS**: Convert to Uzbek Sum
3. Select target currency
4. Enter amount to convert
5. View conversion result


## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/NBU-Bank-Currency-Rates-bot)**