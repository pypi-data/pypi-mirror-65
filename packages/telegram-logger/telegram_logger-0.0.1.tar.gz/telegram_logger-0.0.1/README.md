# Telegram Logger package

This is a simple package, giving you an ability to log directly to Telegram bot [@adv_logger_bot](http://t.me/adv_logger_bot)

## Simple example

First of all, you need to register your project in the [@adv_logger_bot](http://t.me/adv_logger_bot). 

You will get random Token.

In your program, you have to create something like this:

```python
from telegram_logger import TelegramLogger

logger = logging.getLogger(__name__)

f = TelegramLogger(bot_url="<BOT URL>", token="<YOUR TOKEN>>")
logger.addFilter(f)
```

Then on every ```logger.info()```, ```logger.warning()``` or ```logger.error()``` you will get message from bot