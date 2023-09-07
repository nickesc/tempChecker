<h3 align="center" >
  <a href="https://github.com/nickesc/tempChecker"><img alt="Source: Github" src="https://img.shields.io/badge/source-github-brightgreen?style=for-the-badge&logo=github&labelColor=%23505050"></a>
  <br>
  <h3 align="center">
    <code>tempChecker</code>
  </h3>
  <h6 align="center">
    by <a href="https://nickesc.github.io">N. Escobar</a> / <a href="https://github.com/nickesc">nickesc</a>
  </h6>
  <h6 align="center">
    a small project to track the temperature and other <br> conditions in my bedroom and other rooms of my house
  </h6>
</h3>
 

`tempChecker` was born out of a curiosity about the temperature in my room. It always seems to be different than the rest of the house, and I wanted to see whether or not I was just imagining it.

So, I set up a small hardware project to track it using a Feather microcontroller running CircuitPython.

### Requirements:
- 1x [Adafruit ESP32-S2 Feather - 4 MB Flash + 2 MB PSRAM](https://www.adafruit.com/product/5000)
- 1x USB Cable and power source
- a Wifi connection
- an Adafruit IO account

Every 6 minutes, the Feather grabs temperature, humidity and pressure readings from the onboard BME280 sensor.

![The tempChecker sitting on top of my mirror](docs/device.jpeg)

> Here, you can see the microcontroller set up on top of the mirror in my room. It lives there, where it can sit unbothered long term. The red LED on the board lights up while sending data to Adafruit IO so that I know when a reading is being taken.

It sends those readings to Adafruit IO, which logs them and displays them on a [dashboard](https://io.adafruit.com/nickesc/dashboards/room-environment) that I've customized.

![The tempChecker dashboard](docs/dashboard.jpeg)

-----

### Acknowledgments

Much of the `tempChecker` code comes from [this page](https://learn.adafruit.com/adafruit-esp32-s2-feather/i2c-on-board-sensors) from Adafruit on the ESP32-S2 Feather. Code has been modified to work for my use case, but is mostly derived from that guide.

For other information on using the BME280 sensor, see [this guide](https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test) and this [library repository](https://github.com/adafruit/Adafruit_CircuitPython_BME280).
