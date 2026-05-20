#!/usr/bin/env python3

import requests
from datetime import datetime

# Rio de Janeiro
LATITUDE = -22.90
LONGITUDE = -43.20

URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=temperature_2m,"
    "relative_humidity_2m,"
    "apparent_temperature,"
    "pressure_msl,"
    "wind_speed_10m,"
    "weather_code"
    "&daily=sunrise,sunset,"
    "temperature_2m_max,"
    "temperature_2m_min"
    "&timezone=auto"
)


def descricao_clima(codigo_clima):
    descricoes = {
        0: "Céu limpo",
        1: "Principalmente limpo",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Neblina",
        48: "Neblina com geada",
        51: "Garoa leve",
        53: "Garoa moderada",
        55: "Garoa intensa",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        71: "Neve leve",
        80: "Pancadas de chuva leves",
        81: "Pancadas de chuva moderadas",
        82: "Pancadas de chuva fortes",
        95: "Tempestade"
    }

    return descricoes.get(codigo_clima, "Desconhecido")


def formata_hora(date_string):
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%H:%M")


def exibe_clima(data):
    current = data["current"]
    daily = data["daily"]

    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    feels_like = current["apparent_temperature"]
    pressure = current["pressure_msl"]
    wind = current["wind_speed_10m"]
    weather_code = current["weather_code"]

    temp_min = daily["temperature_2m_min"][0]
    temp_max = daily["temperature_2m_max"][0]

    sunrise = formata_hora(daily["sunrise"][0])
    sunset = formata_hora(daily["sunset"][0])

    description = descricao_clima(weather_code)

    print("\n" + "=" * 50)
    print("CLIMA - RIO DE JANEIRO")
    print("=" * 50)

    print(f"\nCondição: {description}")
    print(f"Temperatura: {temp}°C")
    print(f"Sensação térmica: {feels_like}°C")
    print(f"Mínima: {temp_min}°C")
    print(f"Máxima: {temp_max}°C")

    print(f"\nUmidade: {humidity}%")
    print(f"Pressão: {pressure} hPa")

    print(f"\nVento: {wind} km/h")

    print(f"\nNascer do sol: {sunrise}")
    print(f"Pôr do sol: {sunset}")

    alerts = []

    if temp >= 35:
        alerts.append("🔥 Muito calor")

    if temp <= 10:
        alerts.append("🥶 Muito frio")

    if humidity >= 90:
        alerts.append("💧 Umidade muito alta")

    rain_codes = [
        51, 53, 55,
        61, 63, 65,
        80, 81, 82,
        95
    ]

    if weather_code in rain_codes:
        alerts.append("🌧 Possível chuva")

    if alerts:
        print("\nALERTAS:")

        for alert in alerts:
            print(f" - {alert}")

    print("\n" + "=" * 50)


def main():
    try:
        response = requests.get(URL, timeout=10)

        if response.status_code != 200:
            print("Erro ao consultar API.")
            print(response.text)
            return

        data = response.json()

        exibe_clima(data)

    except requests.RequestException as e:
        print(f"Erro de conexão: {e}")


if __name__ == "__main__":
    main()














	
