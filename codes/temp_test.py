#!/usr/bin/env python
"""Lightweight Flask-based fake weather API used for testing/demo.

Provides a single endpoint `/weather` that returns a realistic-looking
temperature and humidity for the requested city/country. Values are
generated randomly (within realistic ranges) so tests can validate
response shapes and ranges without external dependencies.
"""

from typing import Dict, Any
import random
from flask import Flask, jsonify, request


app = Flask(__name__)


def generate_weather(city: str, country: str) -> Dict[str, Any]:
    """Generate a realistic temperature and humidity for the given location.

    Temperature is in degrees Celsius and humidity in percent. Values are
    randomized but kept within realistic ranges.
    """
    # Simple location-based bias — warm climates get higher temps on average.
    warm_countries = {"IN", "AU", "BR", "ZA", "MX"}
    if country and country.upper() in warm_countries:
        base_temp = random.uniform(22.0, 32.0)
    else:
        base_temp = random.uniform(10.0, 25.0)

    # Add daily variation
    temp = round(base_temp + random.uniform(-6.0, 6.0), 1)

    # Humidity realistic between 10% and 100%, biased by temperature
    if temp >= 30:
        humidity = round(random.uniform(30, 80), 1)
    elif temp >= 20:
        humidity = round(random.uniform(40, 85), 1)
    else:
        humidity = round(random.uniform(20, 90), 1)

    # Simple condition inference
    if humidity > 80:
        condition = "Rainy"
    elif temp > 30:
        condition = "Hot"
    elif temp < 5:
        condition = "Cold"
    else:
        condition = "Clear"

    return {
        "location": city or "unknown",
        "temperature_celsius": temp,
        "humidity_percent": humidity,
        "condition": condition,
    }


@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Bangalore")
    country = request.args.get("country", "IN")
    # Allow an optional seed for deterministic responses during tests
    seed = request.args.get("seed")
    if seed is not None:
        try:
            random.seed(int(seed))
        except Exception:
            # ignore invalid seed, continue with random
            pass

    payload = generate_weather(city, country)
    return jsonify(payload)


if __name__ == "__main__":
    # Run locally for manual testing
    app.run(host="127.0.0.1", port=5001, debug=True)