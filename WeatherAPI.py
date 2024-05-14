import requests_cache
import pandas as pd
from retry_requests import retry
import datetime
import openmeteo_requests
class WeatherApiClient:
    def __init__(self, latitude, longitude, timezone, mediator=None):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.mediator = mediator
        self.data = None
        self.last_api_call_time = None
    def send_to_mediator(self, msg):
        self.mediator.receive_message(msg)

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.data = msg.get_data()
            self.process_data()
        #elif channel == '':
            # do thing
        else:
            # Handle other cases if needed
            pass

        #client_id should be the token
    def process_data(self):
        pass
    def get_weather_data(self, variables, forecast_days=1):
        if self.last_api_call_time is None or (datetime.datetime.now() - self.last_api_call_time).total_seconds() > 30 * 60:
            url = "https://api.open-meteo.com/v1/bom"
            params = {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "hourly": ",".join(variables),
                "timezone": "GMT",
                "forecast_days": forecast_days
            }
            responses = self.openmeteo.weather_api(url, params=params)
            self.data = responses
            self.last_api_call_time = datetime.datetime.now()
            return responses
        else:
            return self.data
    def get_metadata(self):
        responses = self.get_weather_data(variables=["temperature_2m"])

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    def get_hourly_data(self):
        responses = self.get_weather_data(variables=["temperature_2m"])
        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        # print(hourly_dataframe)
        return hourly_dataframe

    def get_current_temperature(self):
        df = self.get_hourly_data()
        df['date'] = pd.to_datetime(df['date'])
        current_time_utc = pd.Timestamp.utcnow()
        current_hour_index = df.index[df['date'] == current_time_utc.floor('h')][0]
        # Find the temperature for the hour after the current hour
        temperature = df.at[current_hour_index, 'temperature_2m']
        # print("Temperature for the current hour:", temperature)
        return temperature
    def get_next_hour_temperature(self):
        df = self.get_hourly_data()
        df['date'] = pd.to_datetime(df['date'])
        current_time_utc = pd.Timestamp.utcnow()
        current_hour_index = df.index[df['date'] == current_time_utc.floor('h')][0]
        # Find the temperature for the hour after the current hour
        next_hour_temperature = df.at[current_hour_index + 1, 'temperature_2m']
        # print("Temperature for the hour after the current hour:", next_hour_temperature)
        return next_hour_temperature

# Example usage:
if __name__=="__main__":
    weather_client = WeatherApiClient(latitude=-37.814, longitude=144.9633, timezone="Australia/Sydney")
    weather_client.get_metadata()
    print(weather_client.get_hourly_data())
    print(weather_client.get_next_hour_temperature())
    print(weather_client.get_current_temperature())

    print(weather_client.get_hourly_data())
    print(weather_client.get_next_hour_temperature())
    print(weather_client.get_current_temperature())