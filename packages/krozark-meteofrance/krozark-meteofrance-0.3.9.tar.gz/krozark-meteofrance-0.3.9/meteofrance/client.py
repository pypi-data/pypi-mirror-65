# -*- coding: utf-8 -*-
"""
Meteo France raining forecast.
"""

import re
import requests
import datetime
import string
from bs4 import BeautifulSoup
from pytz import timezone



SEARCH_API = 'http://www.meteofrance.com/mf3-rpc-portlet/rest/lieu/facet/previsions/search/{}'
RAIN_FORECAST_API = 'http://www.meteofrance.com/mf3-rpc-portlet/rest/pluie/{}/'
WEATHER_FORECAST_URL = 'http://www.meteofrance.com/previsions-meteo-france/{}/{}'
WEATHER_FORECAST_WORLD_URL = 'http://www.meteofrance.com/previsions-meteo-monde/{}/{}'


class meteofranceError(Exception):
    """Raise when errors occur while fetching or parsing MeteoFrance data"""


class meteofranceClient():
    """Client to fetch and parse data from Meteo-France"""
    def __init__(self, postal_code, update=False, need_rain_forecast=True, include_today=False):
        """Initialize the client object."""
        self.postal_code = postal_code
        self._city_slug = False
        self._insee_code = False
        self._rain_forecast = False
        self._rain_available = False
        self._weather_html_soup = False
        self.need_rain_forecast = need_rain_forecast
        self.include_today = include_today
        self._type = None
        self._data = {}
        self._init_codes()
        if update:
            self.update()

    def update(self):
        """Fetch new data and format it"""
        self._fetch_foreacast_data()
        if (self._rain_available is True and self.need_rain_forecast is True):
            self._fetch_rain_forecast()
        self._format_data()

    def _init_codes(self):
        """Search and set city slug and insee code."""
        url = SEARCH_API.format(self.postal_code)
        try:
            response = requests.get(url, timeout=10)
            if response.history:
                raise meteofranceError("Error: www.meteofrance.com is overloaded or in maintenance and return a redirection. Unable to get the data from the source.")
        
            elif response.status_code != 200:
                raise meteofranceError("Error: www.meteofrance.com server return an unexpected status code (%s). Unable to get the data from source.", response.status_code)
            
            results = response.json()
            
            for result in results:
                if result["id"] and (result["type"] == "VILLE_FRANCE" or result["type"] == "VILLE_MONDE"):
                    self._insee_code = result["id"]
                    self._data['insee_code']= self._insee_code
                    self._city_slug = result["slug"]
                    self._rain_available = result["pluieAvalaible"]
                    self._data["name"] = result["slug"].title()
                    self._data["printName"] = result["nomAffiche"]
                    self.postal_code = result["codePostal"]
                    self._type = result["type"]
                    if result["parent"] and result["parent"] and result["parent"]["type"] == "DEPT_FRANCE":
                        self._data["dept"] = result["parent"]["id"][4:]
                        self._data["dept_name"] = result["parent"]["nomAffiche"]
                    return
            raise meteofranceError("Error: no forecast for the query `{}`".format(self.postal_code))
        except Exception as err:
            raise meteofranceError(err)

    def _fetch_rain_forecast(self):
        """Get the latest data from Meteo-France."""
        url = RAIN_FORECAST_API.format(self._insee_code)
        try:
            result = requests.get(url, timeout=10).json()
            if result['hasData'] is True:
                self._rain_forecast = result
            else:
                raise meteofranceError("This location has no rain forecast available")
        except Exception as err:
            raise meteofranceError(err)

    def _fetch_foreacast_data(self):
        """Get the forecast and current weather from Meteo-France."""
        if self._type == "VILLE_MONDE":
            url = WEATHER_FORECAST_WORLD_URL.format(self._city_slug, self._insee_code)
        else:
            url = WEATHER_FORECAST_URL.format(self._city_slug, self.postal_code)

        try:
            result = requests.get(url, timeout=10)
            if result.status_code == 200:
                soup = BeautifulSoup(result.text, 'html.parser')
                if soup.find(class_="day-summary-label") is not None:
                    self._weather_html_soup = soup
                    self._parse_insee_code(result.text)
                    return
            raise meteofranceError("Error while fetching weather forecast")
        except Exception as err:
            raise meteofranceError(err)


    def _parse_insee_code(self, html_content):
        insee_code = re.findall('codeInsee:"([^"]*)"', html_content)
        if len(insee_code) is not 0:
            self._insee_code = insee_code[0]

    def _get_next_rain_time(self):
        """Get the minutes to the next rain"""
        time_to_rain = 0
        for interval in self._rain_forecast["dataCadran"]:
            if interval["niveauPluie"] > 1:
                return time_to_rain
            time_to_rain += 5
        return "No rain"

    def _get_next_rain_datetime(self):
        """Get the time of the next rain"""
        # Convert the string in date and time with Europe/Paris timezone.
        string_date = self._rain_forecast["echeance"]
        annee = int(string_date[0:4])
        mois = int(string_date[4:6])
        jour = int(string_date[6:8])
        heure = int(string_date[8:10])
        minute = int(string_date[10:12])
        paris_timezone = timezone("Europe/Paris")
        cadran_start_time = paris_timezone.localize(
            datetime.datetime(annee, mois, jour, heure, minute)
        )

        # Get the delay in minutes until next rain.
        next_rain_delay = self._get_next_rain_time()
        if next_rain_delay == "No rain":
            return "No rain"
        
        # Else Compute the date of the next rain
        return cadran_start_time + datetime.timedelta(minutes=int(next_rain_delay))
        
    def _get_next_sun_time(self):
        """Get the minutes to the next sun"""
        time_to_sun = 0
        for interval in self._rain_forecast["dataCadran"]:
            if interval["niveauPluie"] <= 1:
                return time_to_sun
            time_to_sun += 5
        return 60

    def _format_data(self):
        """Format data from JSON and HTML returned by Meteo-France."""
        try:
            self._data["fetched_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rain_forecast = self._rain_forecast
            if rain_forecast is not False:
                next_rain_datetime = self._get_next_rain_datetime()
                self._data["rain_forecast"] = ''#rain_forecast["niveauPluieText"][0]
                self._data["next_rain"] = self._get_next_rain_time()
                if next_rain_datetime == "No rain":
                    self._data["next_rain_datetime"] = "No rain"
                else: 
                    self._data["next_rain_datetime"] = next_rain_datetime.isoformat()
                emojis = [' ','☀️','🌦','🌧','💦']
                self._data["next_rain_intervals"] = {}
                for interval in range(0, len(rain_forecast["dataCadran"])):
                    self._data["next_rain_intervals"]["rain_level_"+str(interval*5)+"min"] = int(rain_forecast["dataCadran"][interval]["niveauPluie"])
                    self._data["rain_forecast"] += emojis[int(rain_forecast["dataCadran"][interval]["niveauPluie"])]
                if self._data["next_rain"] == 'No rain':
                    self._data["rain_forecast_text"] = "Pas de pluie dans l'heure"
                elif self._data["next_rain"] == 0:
                    self._data["rain_forecast_text"] = "Pluie pendant encore au moins {} min".format(self._get_next_sun_time())
                else:
                    self._data["rain_forecast_text"] = "Risque de pluie à partir de {}".format(next_rain_datetime.strftime("%H:%M"))
            soup = self._weather_html_soup
            if soup is not False:
                self._data["weather"] = soup.find(class_="day-summary-label").string.strip()

                try: #extract classname
                    self._data["weather_class"] = soup.find(class_="day-summary-image").find("span").attrs['class'][1]
                except:
                    self._data["weather_class"] = None

                try:
                    self._data["temperature"] = int(re.sub(r"[^0-9\-]","",soup.find(class_="day-summary-temperature").string))
                except: #weird class name of world pages
                    self._data["temperature"] = int(re.sub(r"[^0-9\-]","",soup.find(class_="day-summary-temperature-outremer").string))

                try:
                    self._data["wind_speed"] = int(next(soup.find(class_="day-summary-wind").stripped_strings).replace(' km/h', ''))
                except: #replace '< 5' by 0
                    self._data["wind_speed"] = 0

                try:
                    self._data["wind_bearing"] = soup.find(class_="day-summary-wind").find("span").attrs['class'][1][2:]
                except: #replace '< 5' by 0
                    self._data["wind_bearing"] = None
                if self._data["wind_bearing"] == "V": #no wind
                    self._data["wind_bearing"] = None

                day_probabilities = soup.find(class_="day-probabilities")
                if day_probabilities:
                    day_probabilities = day_probabilities.find_all("li")
                    self._data["rain_chance"] = int(day_probabilities[0].strong.string.split()[0])
                    self._data["thunder_chance"] = int(day_probabilities[1].strong.string.split()[0])
                    try:
                        self._data["freeze_chance"] = int(day_probabilities[2].strong.string.split()[0])
                    except:
                        self._data["freeze_chance"] = 0
                    try:
                        self._data["snow_chance"] = int(day_probabilities[3].strong.string.split()[0])
                    except:
                        self._data["snow_chance"] = 0

                if soup.find(class_="day-summary-uv").string:
                    self._data["uv"] = int(soup.find(class_="day-summary-uv").string.split()[1])

                self._data["forecast"] = {}
                daydatas = soup.find(class_="liste-jours").find_all("li")
                day = 0
                for daydata in daydatas:
                    try:
                        forecast = {}
                        forecast["date"] = daydata.find("a").string
                        weather = daydata.find("dd").string
                        if weather:
                          forecast["weather"] = weather.strip()
                          min_temp = re.sub(r"[^0-9\-]","",daydata.find(class_="min-temp").string)
                          if min_temp != '-':
                            forecast["min_temp"] = int(min_temp)
                          max_temp = re.sub(r"[^0-9\-]","",daydata.find(class_="max-temp").string)
                          if max_temp != '-':
                            forecast["max_temp"] = int(max_temp)
                          forecast["weather_class"] = daydata.find("dd").attrs['class'][1]
                          if self.include_today:
                            self._data["forecast"][day] = forecast
                          elif day > 0 and day < 6:
                            self._data["forecast"][day-1] = forecast
                        day = day + 1
                    except:
                        raise



        except Exception as err:
            raise meteofranceError("Error while formatting datas: {}".format(err))

    def _format_data_for_day(self):
        """ Format data forecast for the next days"""


    def get_data(self):
        """Return formatted data of current forecast"""
        return self._data
