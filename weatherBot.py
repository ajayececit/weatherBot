
import telebot
from telegram import ReplyKeyboardMarkup
from telebot import types
import telegram
from weatherClass import forecastByCity
from weatherClass import currentWeatherByCity
bot_token = {BOT_TOKEN}
bot = telebot.TeleBot(bot_token)

# Unicodes for Emoji for respective weather code
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

degree_sign= u'\N{DEGREE SIGN}' # degree sign

footer = "------------------------------------------------------------------"

forecastList = []
print ("bfre class")

def inputKeyboard():
    print ("keyClass")
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    markup.add("Current Weather", "ForeCast")
    markup.add("<<Back")
    return markup

def weatherInputKeyboard():
    print ("keyClass")
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Pin Location", "City")
    return markup
    
@bot.message_handler(commands=['start', 'help'])
def handle_command_testMessage(message):
    if (message.text == "/start"):
        bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        @bot.message_handler(regexp='City')
        def handle_command_weather(message):
            if(message.text == "City"):
                echo = bot.reply_to(message,text = "Please provide the city name \n eg:Bangalore,IN")
                bot.register_next_step_handler(echo, processByCityName)
        @bot.message_handler(regexp='Pin Location')
        def handle_command_weather(message):
            if(message.text == "Pin Location"):
                echo = bot.reply_to(message, text = "Please Attach the Location using telegram Maps")
                bot.register_next_step_handler(echo, handle_Location)
            
    if(message.text == "/help"):
        bot.send_message(chat_id=message.chat.id,text = "test success")
        
@bot.message_handler(content_types=['location'])
def handle_Location(message):
    lat = str(message.location.latitude)
    lon = str(message.location.longitude)
    locToPass = lat + "/" + lon
    bot.reply_to(message, text = "Please select the required" ,reply_markup=inputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
    @bot.message_handler(regexp='Current Weather')
    def handle_command_weather(message):
        if(message.text == "Current Weather"):
            weatherOutput = extractDetails(locToPass)
            bot.reply_to(message, text = weatherOutput)
            bot.send_message(chat_id=message.chat.id,text = footer ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        
    @bot.message_handler(regexp='ForeCast')
    def handle_command_weather(message):
        if(message.text == "ForeCast"):
            forecastOutput = []
            forecastOutput = extractForecastDetails(locToPass)
            forecastSplit = forecastOutput[0:3]
            forecastToSend = forecastSplit[0] + forecastSplit [1] + forecastSplit[2]
            bot.reply_to(message, text = forecastToSend)
            bot.send_message(chat_id=message.chat.id,text = footer ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        
    @bot.message_handler(regexp='<<Back')
    def handle_command_weather(message):
        if(message.text == "<<Back"):
            bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        
    
def processByCityName(message):
    cityName = message.text
    bot.reply_to(message, text = "Please select the required" ,reply_markup=inputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
    @bot.message_handler(regexp='Current Weather')
    def handle_command_weather(message):
        if(message.text == "Current Weather"):
            weatherOutput = extractDetails(cityName)
            bot.reply_to(message, text = weatherOutput)
            bot.send_message(chat_id=message.chat.id,text = footer ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        
    @bot.message_handler(regexp='ForeCast')
    def handle_command_weather(message):
        if(message.text == "ForeCast"):
            forecastOutput = []
            forecastOutput = extractForecastDetails(cityName)
            forecastSplit = forecastOutput[0:3]
            forecastToSend = forecastSplit[0] + forecastSplit [1] + forecastSplit[2]
            bot.reply_to(message, text = forecastToSend)
            bot.send_message(chat_id=message.chat.id,text = footer ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
        
    @bot.message_handler(regexp='<<Back')
    def handle_command_weather(message):
        if(message.text == "<<Back"):
            bot.send_message(chat_id=message.chat.id,text = "**Please select from the below menu**" ,reply_markup=weatherInputKeyboard(), parse_mode=telegram.ParseMode.MARKDOWN)
    

def extractDetails(cityDetails):
    try:
        weatherClass = currentWeatherByCity(cityDetails)
        weatherCode = weatherClass.weatherCode
        weatherDesc = weatherClass.weatherDescription
        weatherEmoji = getEmoji(weatherCode)
        currentTemperature = str(weatherClass.currentTemp)
        maxTemperature = str(weatherClass.maxTemp)
        minTemperature = str(weatherClass.minTemp)
        humidity = str(weatherClass.humidity)
        windSpeed = str(weatherClass.windSpeed)
        weatherOutput = "Weather : " + weatherDesc + " " + weatherEmoji  + "\n-> Current Temperature : " + currentTemperature + degree_sign + "C" + "\n-> Max/Min Temperature : " + maxTemperature + degree_sign + "C" + "/" + minTemperature + degree_sign + "C" + "\n-> Humidity : " + humidity + "\n-> Wind Speed : " + windSpeed
    except:
        weatherOutput = "City Not Found"
    return weatherOutput

def extractForecastDetails(cityDetails):
    count = 0
    while(count < 23):
        weatherCode = ""
        weatherDesc = ""
        weatherEmoji = ""
        maxTemperature = ""
        minTemperature = ""
        humidity = ""
        windSpeed = ""
        forecastCollection = ""
        
        forecastClass = forecastByCity(cityDetails ,count)
        weatherDesc = forecastClass.forecastDescription
        weatherEmoji = getEmoji(weatherCode)
        maxTemperature = str(forecastClass.maxTemp)
        minTemperature = str(forecastClass.minTemp)
        humidity = str(forecastClass.humidity)
        windSpeed = str(forecastClass.windSpeed)
        date = str(forecastClass.date)
    	
        forecastCollection = "\nThe weather Report on Date : " + date + "\nWeather : " + weatherDesc + " " + weatherEmoji + "\n->Max/Min Temp : " + maxTemperature + degree_sign + "C" + "/" + minTemperature + degree_sign + "C" + "\n-> Humidity : " + humidity + "\n-> Wind Speed : " + windSpeed + "\n"
        forecastList.append(forecastCollection)
        count = count + 8   

    return forecastList[0:3]
       
def getEmoji(weatherCode):
    if (weatherCode):
        if str(weatherCode)[0] == '2' or weatherCode == 900 or weatherCode==901 or weatherCode==902 or weatherCode==905:
            return thunderstorm
        elif str(weatherCode)[0] == '3':
            return drizzle
        elif str(weatherCode)[0] == '5':
            return rain
        elif str(weatherCode)[0] == '6' or weatherCode==903 or weatherCode== 906:
            return snowflake + ' ' + snowman
        elif str(weatherCode)[0] == '7':
            return atmosphere
        elif weatherCode == 800:
            return clearSky
        elif weatherCode == 801:
            return fewClouds
        elif weatherCode==802 or weatherCode==803 or weatherCode==803:
            return clouds
        elif weatherCode == 904:
            return hot    
    else:
        return defaultEmoji
    
bot.polling()
