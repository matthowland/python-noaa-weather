===========
NOAA Weather
===========

A handy utility to pull weather from NOAA services in a sane manner.

    #!/usr/bin/env python

    from noaaweather import weather

    sfWeather = weather.noaa()
    sfWeather.getByZip('94109')
    print sfWeather.precipitation.liquid.tomorrow.max.value
    print sfWeather.temperature.apparent.tomorrow.min.value
    print sfWeather.temperature.apparent.value
    Support for Temperature, Humidity, Wind, Precipitation, Cloud Cover

    Pulls from http://graphical.weather.gov/xml/rest.php

    First release not really tested...


