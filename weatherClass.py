


import requests
import pandas as pd
import json

degree_sign= u'\N{DEGREE SIGN}' # degree sign
class forecastByCity(object):
    def __init__(self, location ,count):
        openWeatherAPI_key = {API-TOKEN}
        openForecastUrl= "http://api.openweathermap.org/data/2.5/forecast?"
        if (location.find("@#$") == -1):
            openForecastByCity = openForecastUrl + "q=" + location + "&APPID=" + openWeatherAPI_key
        else:
            locationSplit = location.split("@#$")
            latlonConcatenate = "lat=" + locationSplit[0] + "&lon=" + locationSplit[1]                               
            openForecastByCity = openForecastUrl + latlonConcatenate + "&APPID=" + openWeatherAPI_key
            
        forecastData = requests.get(openForecastByCity)
        if (forecastData.status_code ==  200):            
            self.forecastJson = forecastData.json() 
            self.forecastCode = self.__forecastCode(count)
            emojiClass = emoji(self.forecastCode)
            self.weatherEmoji = emojiClass.smiley
            self.forecastDescription = str(self.__forecastDescription(count))
            self.maxTemp = str(self.__maxTemp(count))
            self.minTemp = str(self.__minTemp(count))
            self.humidity= str(self.__humidity(count))
            self.windSpeed = str(self.__windSpeed(count))
            self.date = str(self.__date(count))
            self.forecastCollection = "\nThe weather Report on Date : " + self.date + "\nWeather : " + self.forecastDescription + " " + self.weatherEmoji + "\n->Max/Min Temp : " + self.maxTemp + degree_sign + "C/" + self.minTemp + degree_sign + "C" + "\n-> Humidity : " + self.humidity + "\n-> Wind Speed : " + self.windSpeed + "\n"            

        elif(forecastData.status_code == 401):
            self.forecastCollection = "Issue with API key"
        elif(forecastData.status_code == 404):
            self.forecastCollection = "City not found"        
    
    def __forecastCode(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        idTable = forecastDataFrame.iloc[count]["weather"]
        IdFrame = pd.DataFrame(idTable)
        return IdFrame.iloc[0]["id"]
    
    def __forecastDescription(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        idTable = forecastDataFrame.iloc[count]["weather"]
        IdFrame = pd.DataFrame(idTable)
        return IdFrame.iloc[0]["description"]
    
    def __currentTemp(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        currentTemp = (forecastDataFrame.iloc[count]["main"])
        return (round(currentTemp["temp"] -273.15 , 2))
    
    def __windSpeed(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        windSpeed =  (forecastDataFrame.iloc[count]["wind"])    
        return windSpeed["speed"]
    
    def __humidity(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        humidity = (forecastDataFrame.iloc[count]["main"])
        return humidity["humidity"]
    
    def __maxTemp(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        maxTemp = (forecastDataFrame.iloc[count]["main"])
        return (round(maxTemp["temp_max"]-273.15 , 2))
            
    def __minTemp(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        minTemp =  (forecastDataFrame.iloc[count]["main"])
        return (round(minTemp["temp_min"]-273.15 , 2))
      
    def __date(self,count):
        forecastTable = self.forecastJson["list"]
        forecastDataFrame = pd.DataFrame(forecastTable)
        date = (forecastDataFrame.iloc[count]["dt_txt"])
        date = date.split(" ")
        return date[0]
    
class currentWeatherByCity(object):
    def __init__(self, location): 
        openWeatherAPI_key = "f0983710160711b7b3010621ea077e80"
        openWeatherUrl= "http://api.openweathermap.org/data/2.5/weather?"
        if (location.find("@#$") == -1):
            openWeatherByCity = openWeatherUrl + "q=" + location + "&APPID=" + openWeatherAPI_key
        else:
            locationSplit = location.split("@#$")
            latlonConcatenate = "lat=" + locationSplit[0] + "&lon=" + locationSplit[1]
            openWeatherByCity = openWeatherUrl + latlonConcatenate + "&APPID=" + openWeatherAPI_key
        
        weatherData = requests.get(openWeatherByCity)
        if (weatherData.status_code ==  200):            
            self.weatherJson = weatherData.json()  
            self.weatherCode = self.__weatherCode()
            self.weatherDescription = self.__weatherDescription()
            emojiClass = emoji(self.weatherCode)
            self.weatherEmoji = emojiClass.smiley
            self.currentTemp = str(self.__currentTemp())
            self.maxTemp = str(self.__maxTemp())
            self.minTemp = str(self.__minTemp())
            self.humidity= str(self.__humidity())
            self.windSpeed = str(self.__windSpeed())
            self.weatherOutput = "Weather : " + self.weatherDescription + " " + self.weatherEmoji  + "\n-> Current Temperature : " + self.currentTemp + degree_sign + "C" + "\n-> Max/Min Temperature : " + self.maxTemp + degree_sign + "C" + "/" + self.minTemp + degree_sign + "C" + "\n-> Humidity : " + self.humidity + "\n-> Wind Speed : " + self.windSpeed
        elif(weatherData.status_code == 401):
            self.weatherOutput = "Issue with API key"
        elif(weatherData.status_code == 404):
            self.weatherOutput = "City not found"
        
    def __weatherCode(self):
        weatherTable = self.weatherJson["weather"]
        weatherDataFrame = pd.DataFrame(weatherTable)
        return (weatherDataFrame.iloc[0]['id'])
    
    def __weatherDescription(self):
        weatherTable = self.weatherJson["weather"]
        weatherDataFrame = pd.DataFrame(weatherTable)
        return (weatherDataFrame.iloc[0]['description'])
        
    def __currentTemp(self):
        return (round(self.weatherJson['main']['temp']-273.15 , 2))
    
    def __maxTemp(self):
        return (round(self.weatherJson['main']['temp_max']-273.15 , 2))
    
    def __minTemp(self):
        return (round(self.weatherJson['main']['temp_min']-273.15 , 2))
    
    def __humidity(self):
        return (self.weatherJson['main']['humidity'])
    
    def __windSpeed(self):
        return (self.weatherJson['wind']['speed'])
    
class emoji(object):
    
    def __init__(self, weatherCode):
        self.smiley = self.__getSmiley(weatherCode)       
        
    def __getSmiley(self,weatherCode):
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
    
    
