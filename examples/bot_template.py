"""Simple IRChat bot template

Usage: python examples/bot_template.py
"""
from irc_client import IRCClient
import time

class EchoBot(IRCClient):
    def on_message(self, channel, user, message):
        # Simple responder: echo messages that mention the bot
        if 'echo' in message.lower():
            self.send_message(channel, f"{user}: I heard '{message}'")

if __name__ == '__main__':
    bot = EchoBot()
    bot.connect('irc.libera.chat', 6667, 'echobot')
    bot.join_channel('#test')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.disconnect()
        print('Bot stopped')
