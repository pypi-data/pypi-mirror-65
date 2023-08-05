# pip3 install python-telegram-bot
# BotFather /setprivacy disable
# add to group

import telegram

class Telegram:
    def __init__ (self, token):
        self.token = token
        self.bot = telegram.Bot(token = token)

    def show_messages (self):
        updates = self.bot.getUpdates()
        for u in updates:
            print(u.message)

    def updates (self):
        return self.bot.getUpdates()

    def send (self, msg, chat_id = None):
        self.bot.sendMessage (
            chat_id or self.updates ()[-1].message.chat.id,
            msg
        )


if __name__ == "__main__":
    import sys, os
    from telegram.error import TimedOut
    token = os.environ ['TELEGRAM_TOKEN']
    bot = Telegram (token)
    for i in range (3):
        try:
            bot.send (' '.join (sys.argv [1:]))
        except TimedOut:
            time.sleep (2)
            continue
        break
