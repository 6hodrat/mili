from ast import arg
from bdb import set_trace
from email import message
from telegram.ext import Updater , CommandHandler , CallbackContext , MessageHandler , CallbackQueryHandler , ConversationHandler , InlineQueryHandler
from telegram.ext.filters import Filters
from telegram import ReplyKeyboardMarkup , Update , InlineKeyboardMarkup , InlineKeyboardButton , InputTextMessageContent , InlineQueryResultArticle , ParseMode
from telegram.chataction import ChatAction
from uuid import uuid4
import requests
from bs4 import BeautifulSoup
import re
import pdb
from time import sleep


messages = {
    'start':'سلام %s عزیز \n به ربات خوش آمدید.',
    'safhe_asli':'صفحه اصلی:',
    'sazande':'سازنده ربات: \n @Dual_H',

    
    
    'btn_sazande':'سازنده ربات',
    'btn_bagasht':'بازگشت'
}





def start_handler(update:Update , context: CallbackContext):
    if context.args ==['51165116' , '01']:
        chat_id = update.message.chat_id
        context.bot.send_chat_action(chat_id,ChatAction.TYPING)
        # context.bot.sendMessage(chat_id , messages['start'] % update.message.chat.first_name ,update.message.chat.last_name)
        #کار بالایی و پایینی یکیه ولی پایینی راحت تره
        update.message.reply_text(messages['start'] % update.message.chat.first_name ,update.message.chat.last_name)
        safhe_asli_handler(update,context)

def safhe_asli_handler(update:Update , context:CallbackContext):
    buttons = [
        [messages['btn_sazande']]
    ]
    update.message.reply_text(
        messages['safhe_asli'],
        reply_markup=ReplyKeyboardMarkup(buttons , resize_keyboard=True)
    )

def safhe_sazande_handler(update:Update,context:CallbackContext):
    buttons = [ [messages['btn_bagasht']]]
    update.message.reply_text(
        messages['sazande'],
        reply_markup=ReplyKeyboardMarkup(buttons , resize_keyboard=True , one_time_keyboard=True)
    )
    
def bazgasht_handler(update:Update, context:CallbackContext):
    safhe_asli_handler(update,context)

def inline_query_handler(update: Update, context: CallbackContext):
    query = update.inline_query.query
    query_s = query.split(' ')


    if query_s[0] == 'digi':
    
        if len(query_s) !=1 :
            digimovie_url = 'https://digimovie.one/?s=' + query_s[1]
            if len(query_s) >= 2:
                for i in range(2 , len(query_s)):
                    i
                    digimovie_url += '+'+query_s[i]
            
            digimovie = requests.get(digimovie_url)
            soup = BeautifulSoup(digimovie.content, "html.parser")
            film_ha = str(soup.find_all("h2", attrs={"class": 'lato_font iranYekanReg' }))
            film_title =re.findall(r'title=\"(.*?)\"', film_ha)
            film_link = re.findall(r'href=\"(.*?)\" title=\"(.*?)\"', film_ha)
            result = [
                InlineQueryResultArticle(
                        id=uuid4(),
                        title="لیست فیلم ها:",
                        input_message_content=InputTextMessageContent('روی این کلیک نکن')
                    )
                ]
            for i in range(0 ,len(film_title)):
                i-=1
                result += [
                    InlineQueryResultArticle(
                            id=uuid4(),
                            title=str(film_title[i]),
                            input_message_content=InputTextMessageContent(str(film_link[i]))
                    )
                ]
        else:
            result = [
                InlineQueryResultArticle(
                id=uuid4(),
                title="نام را تایپ کنید...",
                input_message_content=InputTextMessageContent('...')
                )
            ]


    if query_s[0] == 'mobo':
          
        if len(query_s) !=1 :
            query_mobomovie = query.replace('mobo ', '')
            mobomovie_url = 'https://mobomovie1.xyz/search/' + query_mobomovie
            
            
            mobomovie = requests.get(mobomovie_url)
            soup = BeautifulSoup(mobomovie.content, "html.parser")
            film_ha = str(soup.find_all("header", attrs={"class": 'item-h' }))
            film_title =re.findall(r'class=\"permalink d-inline ml-05\">(.*?)<', film_ha)
            film_link = re.findall(r'href=\"(.*?)\"', film_ha)
            result = [
                InlineQueryResultArticle(
                id=uuid4(),
                title="لیست فیلم ها:",
                input_message_content=InputTextMessageContent('روی این کلیک نکن')
                )
            ]

            for i in range(0 ,len(film_title)):
                result += [
                    InlineQueryResultArticle(
                            id=uuid4(),
                            title=str(film_title[i]),
                            input_message_content=InputTextMessageContent(str(film_link[i]))
                    )
                ]
        else:
            result = [
                InlineQueryResultArticle(
                id=uuid4(),
                title="نام را تایپ کنید...",
                input_message_content=InputTextMessageContent('...')
                )
            ]


    if query_s[0] != 'mobo' and query_s[0] != 'digi':
        result = [
            InlineQueryResultArticle(
            id=uuid4(),
            title="...",
            input_message_content=InputTextMessageContent(query)
            )
        ]


        
    

    update.inline_query.answer(result)

def main():
    updater = Updater("5336665025:AAEbJoezMTIlpHpyC5mkEZhAG6XyblhhjuM" , use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start" , start_handler ,pass_args=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages['btn_bagasht']) ,bazgasht_handler ))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages['btn_sazande']) ,safhe_sazande_handler))

    updater.dispatcher.add_handler(InlineQueryHandler(inline_query_handler))


    updater.start_polling()
    updater.idle()





main()
