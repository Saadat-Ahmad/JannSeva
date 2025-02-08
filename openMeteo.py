import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

global daily_sunshine_duration
global hourly_dataframe

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"

def main(lat, lng):
	params = {
		"latitude": lat,
		"longitude": lng,
		"start_date": "2025-01-23",
		"end_date": "2025-02-06",
		"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "snowfall", "pressure_msl", "cloud_cover", "et0_fao_evapotranspiration", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
		"daily": "sunshine_duration",
		"timezone": "auto"
	}

	responses = openmeteo.weather_api(url, params=params)

	response = responses[0]

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
	hourly_rain = hourly.Variables(4).ValuesAsNumpy()
	hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
	hourly_pressure_msl = hourly.Variables(6).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
	hourly_et0_fao_evapotranspiration = hourly.Variables(8).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(9).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(10).ValuesAsNumpy()
	hourly_wind_gusts_10m = hourly.Variables(11).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["dew_point_2m"] = hourly_dew_point_2m
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["rain"] = hourly_rain
	hourly_data["snowfall"] = hourly_snowfall
	hourly_data["pressure_msl"] = hourly_pressure_msl
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
	hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	#print(hourly_dataframe)

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_sunshine_duration = daily.Variables(0).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	return [daily_sunshine_duration, hourly_dataframe]
	# daily_data["sunshine_duration"] = daily_sunshine_duration
	# daily_dataframe = pd.DataFrame(data = daily_data)
	# print(daily_sunshine_duration)
    

def sunshine(lat, lng):
    data = main(lat, lng)
    return data[0]

def weather(lat, lng):
    data = main(lat, lng)
    return data[1]

print(weather(27.9445504, 78.0828672))