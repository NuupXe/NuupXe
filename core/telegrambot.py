import ConfigParser
import logging
import telebot

class TelegramBot():

    def __init__(self):
        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read('configuration/services.config')
        self.token = self.configuration.get('telegram','token')
        self.mybot = telebot.TeleBot(self.token)

    def listener(self, message):
        for m in message:
            chatid = m.chat.id
            if m.content_type == 'text':
                text = ascii_ignore(m.text)
                if m.text == '/date':
                    self.mybot.send_message(chatid, text)
                    self.mybot.send_message(chatid, "The date is ...")

    def execute(self):
        self.mybot.set_update_listener(self.listener)
        self.mybot.polling()
        while True:
            pass

if __name__ == "__main__":

    telegrambot = TelegramBot()
    telegrambot.execute()
