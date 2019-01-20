

import telebot
from telegram import ReplyKeyboardMarkup
from telebot import types
import telegram
from weatherClass import forecastByCity
from weatherClass import currentWeatherByCity
bot_token = {BOT_TOKEN}
bot = telebot.TeleBot(bot_token)
degree_sign= u'\N{DEGREE SIGN}' # degree sign


print ("bfre class")

class keyBoardClass():
    
    def inputKeyboard():
        print ("keyClass")
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        markup.add("Current Weather", "ForeCast")
        return markup
    
    def forecastInputKeyboard():
        print ("keyClass")
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
        markup.add("LOCATION", "CITYNAME")
        return markup
    
    def startKeypad():
        print ("keyClass")
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        markup.add("/start")
        return markup
    
    def weatherInputKeyboard():
        print ("keyClass")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("LOCATION", "CITYNAME")
        return markup
    
class botClass(object):
    
    @bot.message_handler(commands=['start'])
    def handle_command_startMessage(message):    
        if (message.text == "/start"):
            bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=keyBoardClass.inputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
            @bot.message_handler(regexp='Current Weather')
            def handle_command_currentWeather(message):
                if(message.text == "Current Weather"):
                    echoForCurrentInput = bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=keyBoardClass.forecastInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
                    bot.register_next_step_handler(echoForCurrentInput, currentLocation)
            def currentLocation(message):
                if(message.text == "LOCATION"):
                    echoLocationCurrent = bot.reply_to(message, text = "Please attach the location using telegram Maps")
                    bot.register_next_step_handler(echoLocationCurrent, processByLocNameCurrent)    
                if(message.text == "CITYNAME"):
                    echo= bot.reply_to(message, text = "Please provide the city name \n eg:Bangalore,IN")
                    bot.register_next_step_handler(echo, processByCityNameCurrent)                        
            def processByLocNameCurrent(message):
                lat = str(message.location.latitude)
                lon = str(message.location.longitude)
                locToPass = ""
                locToPass = lat + "@#$" + lon
                extractionClass = currentWeatherByCity(locToPass)
                weatherOutput = extractionClass.weatherOutput
                bot.send_message(chat_id=message.chat.id, text = weatherOutput,reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
           
            def processByCityNameCurrent(message):
                cityName = message.text
                if (cityName.find(",") == -1):
                    bot.send_message(chat_id=message.chat.id, text = "Please Provide the proper input Name with country code\nEg:Bangalore,IN",reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    extractionClass = currentWeatherByCity(cityName)
                    weatherOutput = extractionClass.weatherOutput    
                    bot.send_message(chat_id=message.chat.id, text = weatherOutput,reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
    
            @bot.message_handler(regexp='ForeCast')
            def handle_command_forecastWeather(message):
                if(message.text == "ForeCast"):
                    echoForForecastInput = bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=keyBoardClass.forecastInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
                    bot.register_next_step_handler(echoForForecastInput, foreCastLocation)
            def foreCastLocation(message):
                if(message.text == "LOCATION"):
                    echoLocationForecast = bot.reply_to(message, text = "Please attach the location using telegram Maps")
                    bot.register_next_step_handler(echoLocationForecast, processByLocNameForecast)    
                if(message.text == "CITYNAME"):
                    echo= bot.reply_to(message, text = "Please provide the city name \n eg:Bangalore,IN")
                    bot.register_next_step_handler(echo, processByCityNameForecast)                        
            def processByLocNameForecast(message):
                lat = str(message.location.latitude)
                lon = str(message.location.longitude)
                locToPass = ""
                locToPass = lat + "@#$" + lon
                count = 0
                forecastList = []
                while(count < 23):
                    extractionClass = forecastByCity(locToPass,count)
                    forecastoutput = extractionClass.forecastCollection
                    forecastList.append(forecastoutput)
                    count = count + 8
                forecastSplit = forecastList[0:3]
                forecastToSend = forecastSplit[0] + forecastSplit [1] + forecastSplit[2]
                bot.send_message(chat_id=message.chat.id, text = forecastToSend,reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
           
            def processByCityNameForecast(message):
                cityName = message.text
                if (cityName.find(",") == -1):
                    bot.send_message(chat_id=message.chat.id, text = "Please Provide the proper input Name with country code\nEg:Bangalore,IN",reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    count = 0
                    forecastList = []
                    while(count < 23):
                        extractionClass = forecastByCity(cityName,count)
                        forecastoutput = extractionClass.forecastCollection
                        forecastList.append(forecastoutput)
                        count = count + 8
                    forecastSplit = forecastList[0:3]
                    forecastToSend = forecastSplit[0] + forecastSplit [1] + forecastSplit[2]
                    bot.send_message(chat_id=message.chat.id, text = forecastToSend,reply_markup=keyBoardClass.startKeypad(), parse_mode=telegram.ParseMode.MARKDOWN)
    bot.polling()
if __name__ == '__main__':
    botClass()
    
