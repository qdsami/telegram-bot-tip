import logging
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps
from typing import Final
from telegram import Update, User
from io import BytesIO
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater
TOKEN: Final = 'TOKEN'
BOT_USERNAME: Final = '@potipai_bot'


my_list = ["test", "2"]

BACKGROUND_IMAGE_PATH: Final[str] = 'img.png'
TEMP_IMAGE_PATH: Final[str] = 'sample-out.jpg'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Помощь /help')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Пиши /tip @ник')
   


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    background_image = Image.open(BACKGROUND_IMAGE_PATH)
    text: str = update.message.text
    print(text+' ')


    user = update.effective_user  # Имя пользователя, который отправил команду
    entities = update.message.entities

    user_name = f'@{user.username}' if user and user.username else user.first_name
    tipnick = text.split()

    if len(tipnick) >= 2:
        user_nickname = tipnick[1]
        #print(user_nickname)
    else:
        await update.message.reply_text('Правильное использование команды: /tip @Qdsami')

    img = Image.open("img.png")
    img = ImageOps.expand(img, border=10, fill=(255,255,255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FONTS/arial.ttf", 36)
    draw.text((30,230),user_name,(1, 120, 250),font=font)
    draw.text((580,230),user_nickname,(1, 238, 2),font=font)
    img.save('tip-out.png')
    
    
    # Сохраняем временное изображение
    img.save(TEMP_IMAGE_PATH)
    await update.message.reply_photo(photo=open(TEMP_IMAGE_PATH, 'rb'), caption=user_name +' благодарит ' + user_nickname + '. Хорошая игра!')

    # Тут хотел сделать как доте, ограничение в день на похвалы


    # for i in range(len(my_list)):
    #     print(f({my_list[i]}))
    #     if user_name == my_list[i]: 
    #         print(f"Пользователя")
    #         if my_list[i] <= 3:
    #             print(f"По идее типнул когто")
    #             await update.message.reply_photo(photo=open(TEMP_IMAGE_PATH, 'rb'), caption=user_name +' благодарит ' + user_nickname + '. Хорошая игра!')
    #             my_list[i] = my_list[i] + 1
    #             break
    #         else:
    #             print(f"Не типнул, лимит")
    #             await update.message.reply_text('Кончились твои типы(((')
    #             break
    #     else:
    #         await update.message.reply_photo(photo=open(TEMP_IMAGE_PATH, 'rb'), caption=user_name +' благодарит ' + user_nickname + '. Хорошая игра!')
    #         print(f"Новый пользователь")
    #         for iq in my_list:
    #             print(iq, end=' ')
    #         my_list.append(user_name)
    #         my_list.append(0)
    img.close()


    await update.message.reply_text(reply_text)


def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    #Это для сообщения лично боту, а не в группах
    if 'привет бот' in processed:
        return 'И тебе привет!'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "({text})"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot', response)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #print(f'Update {update} caused error {context.error}')
    print("________")


#Команды на которые реагирует /start /help /tip
if __name__ == '__main__':
    print('Starting')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('tip', custom_command))

    
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling')
    app.run_polling(poll_interval=1)