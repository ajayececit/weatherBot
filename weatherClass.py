
import requests
import pandas as pd
import json

class forecastByCity(object):
    
    def __init__(self, location ,count):
        openWeatherAPI_key = {YOUR_API}
        openForecastUrl= "http://api.openweathermap.org/data/2.5/forecast?"
        if (location.find("@#$") == -1):
            openForecastByCity = openForecastUrl + "q=" + location + "&APPID=" + openWeatherAPI_key
        else:
            locationSplit = location.split("/")
            latlonConcatenate = "lat=" + locationSplit[0] + "&lon=" + locationSplit[1]                               
            openForecastByCity = openForecastUrl + latlonConcatenate + "&APPID=" + openWeatherAPI_key
            
        forecastData = requests.get(openForecastByCity)
        if (forecastData.status_code ==  200):            
            self.forecastJson = forecastData.json() 
            self.forecastCode = self.__forecastCode(count)
            self.forecastDescription = self.__forecastDescription(count)
            self.currentTemp = self.__currentTemp(count)
            self.maxTemp = self.__maxTemp(count)
            self.minTemp = self.__minTemp(count)
            self.humidity= self.__humidity(count)
            self.windSpeed = self.__windSpeed(count)
            self.date = self.__date(count)

        elif(forecastData.status_code == 401):
            return "Issue with API key"
        elif(forecastData.status_code == 404):
            return "Page not found"        
    
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
            self.currentTemp = self.__currentTemp()
            self.maxTemp = self.__maxTemp()
            self.minTemp = self.__minTemp()
            self.humidity= self.__humidity()
            self.windSpeed = self.__windSpeed()
        elif(weatherData.status_code == 401):
            return "Issue with API key"
        elif(weatherData.status_code == 404):
            return "Page not found"
        
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
    
    
