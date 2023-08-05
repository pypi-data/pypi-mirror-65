import logging
import time

from flask import current_app
from pyowm import OWM
from pyowm.exceptions.api_call_error import APIInvalidSSLCertificateError
from pyowm.exceptions.api_response_error import UnauthorizedError

from flirror.exceptions import CrawlerDataError
from flirror.modules import FlirrorModule


LOGGER = logging.getLogger(__name__)

WEATHER_ICONS = {
    "01d": "wi wi-day-sunny",
    "02d": "wi wi-day-cloudy",
    "03d": "wi wi-cloud",
    "04d": "wi wi-cloudy",
    "09d": "wi wi-day-showers",
    "10d": "wi wi-day-rain",
    "11d": "wi wi-day-thunderstorm",
    "13d": "wi wi-day-snow",
    "50d": "wi wi-dust",
    "01n": "wi wi-night-clear",
    "02n": "wi wi-night-alt-cloudy",
    "03n": "wi wi-cloud",
    "04n": "wi wi-cloudy",
    "09n": "wi wi-night-showers-rain",
    "10n": "wi wi-night-rain",
    "11n": "wi wi-night-thunderstorm",
    "13n": "wi wi-night-snow",
    "50n": "wi wi-dust",
}

# TODO (felix): Define some default values in FlirrorModule?
weather_module = FlirrorModule("weather", __name__, template_folder="templates")


# A template filter to find the correct weather icon by name
@weather_module.app_template_filter()
def weather_icon(icon_name):
    return WEATHER_ICONS.get(icon_name)


@weather_module.view()
def get():
    return current_app.basic_get(template_name="weather/index.html")


@weather_module.crawler()
def crawl(module_id, app, api_key, language, city, temp_unit):
    WeatherCrawler(module_id, app, api_key, language, city, temp_unit).crawl()


class WeatherCrawler:
    def __init__(self, module_id, app, api_key, language, city, temp_unit):
        self.module_id = module_id
        self.app = app
        self.api_key = api_key
        self.language = language
        self.city = city
        self.temp_unit = temp_unit
        self._owm = None

    def crawl(self):
        try:
            obs = self.owm.weather_at_place(self.city)
        except UnauthorizedError as e:
            LOGGER.error("Unable to authenticate to OWM API")
            raise CrawlerDataError from e
        # Despite the name, this exception seem to be raised if no connection is possible
        # at all (e.g. no network/internet connection).
        except APIInvalidSSLCertificateError:
            raise CrawlerDataError("Could not connect to OWM API")

        # Get today's weather and weekly forecast
        LOGGER.info("Requesting weather data from OWM for city '%s'", self.city)
        now = time.time()
        weather = obs.get_weather()

        weather_data = self._parse_weather_data(weather, self.temp_unit, self.city)

        # Get the forecast for the next days
        fc = self.owm.daily_forecast(self.city, limit=7)

        # Skip the first element as we already have the weather for today
        for fc_weather in list(fc.get_forecast())[1:]:
            fc_data = self._parse_forecast_data(fc_weather, self.temp_unit)
            weather_data["forecasts"].append(fc_data)

        # Store the crawl timestamp
        weather_data["_timestamp"] = now

        self.app.store_module_data(self.module_id, weather_data)

    @property
    def owm(self):
        if self._owm is None:
            LOGGER.debug("Authenticating to OWM API")
            self._owm = OWM(API_key=self.api_key, language=self.language, version="2.5")
        return self._owm

    @staticmethod
    def _parse_weather_data(weather, temp_unit, city):
        temp_dict = weather.get_temperature(unit=temp_unit)
        return {
            "city": city,
            "date": weather.get_reference_time(),
            "temp_cur": temp_dict["temp"],
            "temp_min": temp_dict["temp_min"],
            "temp_max": temp_dict["temp_max"],
            "status": weather.get_status(),
            "detailed_status": weather.get_detailed_status(),
            "sunrise_time": weather.get_sunrise_time(),
            "sunset_time": weather.get_sunset_time(),
            # TODO For the forecast we don't need the "detailed" icon
            #  (no need to differentiate between day/night)
            "icon": weather.get_weather_icon_name(),
            "forecasts": [],
        }

    @staticmethod
    def _parse_forecast_data(forecast, temp_unit):
        temperature = forecast.get_temperature(unit=temp_unit)
        return {
            "date": forecast.get_reference_time(),
            "temp_day": temperature["day"],
            "temp_night": temperature["night"],
            "status": forecast.get_status(),
            "detailed_status": forecast.get_detailed_status(),
            # TODO For the forecast we don't need the "detailed" icon
            #  (no need to differentiate between day/night)
            "icon": forecast.get_weather_icon_name(),
        }
