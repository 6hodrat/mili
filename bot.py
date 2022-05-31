import requests
from telegram.ext import Updater , CommandHandler , CallbackContext , MessageHandler
from telegram import ReplyKeyboardMarkup , Update , InlineKeyboardMarkup , InlineKeyboardButton , InputTextMessageContent , ParseMode
from telegram.ext.filters import Filters
from bs4 import BeautifulSoup
import re
messages = {
    'start':'سلام %s عزیز \n به ربات خوش آمدید.',
    'safhe_asli':'صفحه اصلی:',
    'sazande':'سازنده ربات: \n @Dual_H',
    'listesite':'اخرین لینک سایت ها تا این لحظه: \n دیجی مووی:%s \n آوا مووی:%s \n مووی کاتیج:%s \n سرمووی:%s \n فیلم2مدیا:%s \n فیلم2سان:%s \n موبومووی:%s \n الماس مووی:%s \n مای مووی فیلم:%s \n هستی دی ال:%s \n ',
    'error_url_code':'صفحه مورد نظر با ارور %i باز نشد.',
    
    'btn_sazande':'سازنده ربات',
    'btn_bagasht':'بازگشت',
    'btn_listesite':'لیست سایت های فیلم'
}
urls={
    'digimovie':'https://digimovie.one/',
    'avamovie': 'https://avamovie12.xyz/',
    'moviecottage':'https://moviecottage1.fun/',
    'sermovie':'https://sermovie.online/',
    'film2media':'https://www.f2m.site/',
    'film2sun':'https://film2sun.fun/',
    'mobomovie':'https://mobomoviez1.site/',
    'almasmovie':'https://10almasmovie.xyz/',
    'mymoviefilm':'https://mfmovie.xyz/',
    'hastidl':'http://myhastidl.cam/',
}
def bazgasht_handler(update:Update, context:CallbackContext):
    safhe_asli_handler(update,context)

def safhe_asli_handler(update:Update , context:CallbackContext):
    buttons = [ [messages['btn_listesite']],
        [messages['btn_sazande']]
    ]
    update.message.reply_text(
        messages['safhe_asli'],
        reply_markup=ReplyKeyboardMarkup(buttons , resize_keyboard=True)
    )

def safhe_sazande_handler(update:Update,context:CallbackContext):
    buttons = [ 
        [messages['btn_bagasht']]
    ]
    update.message.reply_text(
        messages['sazande'],
        reply_markup=ReplyKeyboardMarkup(buttons , resize_keyboard=True , one_time_keyboard=True)
    )

def start_handler(update:Update , context: CallbackContext):
    if context.args ==['51165116' , '01']:
        chat_id = update.message.chat_id
        # context.bot.sendMessage(chat_id , messages['start'] % update.message.chat.first_name ,update.message.chat.last_name)
        #کار بالایی و پایینی یکیه ولی پایینی راحت تره
        update.message.reply_text(messages['start'] % update.message.chat.first_name ,update.message.chat.last_name)
        safhe_asli_handler(update,context)

def listesite_handler(update:Update,context:CallbackContext):
    for url in urls:
        m = requests.get(urls[url])
        if m.status_code == 200:
            urls[url]=m.url
    mini_msg = messages['listesite']% (urls['digimovie'] , urls['avamovie'] ,urls['moviecottage'],urls['sermovie'],urls['film2media'],urls['film2sun'],urls['mobomovie'],urls['almasmovie'],urls['mymoviefilm'],urls['hastidl'])
    update.message.reply_text(mini_msg)

def digi_handler(update:Update,context:CallbackContext):
    digimovie_url = urls['digimovie'] +'?s='+ context.args[0]
    if len(context.args) >= 1:
                    for i in range(1 , len(context.args)):
                        digimovie_url += '+'+context.args[i]
    digimovie = requests.get(digimovie_url)
    if digimovie.status_code == 200:
        soup = BeautifulSoup(digimovie.content, "html.parser")
        film_ha = str(soup.find_all("h2", attrs={"class": 'lato_font iranYekanReg' }))
        film_title =re.findall(r'title=\"(.*?)\"', film_ha)
        film_link = re.findall(r'href=\"(.*?)\"', film_ha)
        temp_msg=''
        for i in range(0 ,len(film_title)):
            temp_msg+=film_title[i]+': \n'+film_link[i]+'\n \n'
        
        update.message.reply_text(temp_msg)
    else:
        temp_msg=messages['error_url_code'] %(digimovie.status_code)
        update.message.reply_text(temp_msg)




def mobo_handler(update:Update,context:CallbackContext):
    pass




updater = Updater("5336665025:AAEbJoezMTIlpHpyC5mkEZhAG6XyblhhjuM" , use_context=True)
updater.dispatcher.add_handler(CommandHandler("start" , start_handler ,pass_args=True))
updater.dispatcher.add_handler(CommandHandler("digi" , digi_handler ,pass_args=True))
updater.dispatcher.add_handler(CommandHandler("mobo" , mobo_handler ,pass_args=True))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages['btn_bagasht']) ,bazgasht_handler ))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages['btn_sazande']) ,safhe_sazande_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(messages['btn_listesite']) ,listesite_handler ))


updater.start_polling()
updater.idle()