
import os
import time
import ssl
import alarm
import board
import digitalio
import wifi
import socketpool
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
from adafruit_bme280 import basic as adafruit_bme280
try:
    secrets = {
        "ssid": os.getenv("WIFI_SSID"),
        "password": os.getenv("WIFI_PASSWORD"),
        "aio_username": os.getenv("ADAFRUIT_IO_USERNAME"),
        "aio_key": os.getenv("ADAFRUIT_IO_KEY"),
    }
except ImportError:
    print("WiFi and Adafruit IO credentials are kept in settings.toml, please add them there!")
    raise

# Time between grabbing and sending readings to allow the board to cool
sleep_duration = 360

# LED Setup
class LED:
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()

    def on(self):
        self.led.value = True

    def off(self):
        self.led.value = False
led = LED()


# Set up the BME280 and LC709203 sensors
i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Collect the sensor data values and format the data
loggedData = {
    "bme280-temperature":"{:.2f}".format(bme280.temperature),
    "bme280-temperature-f":"{:.2f}".format((bme280.temperature * (9 / 5) + 32)),  # Convert C to F
    "bme280-humidity":"{:.2f}".format(bme280.relative_humidity),
    "bme280-pressure":"{:.2f}".format(bme280.pressure)
}

class IOConnection:

    feeds = {"bme280-temperature":None, "bme280-temperature-f":None, "bme280-humidity":None, "bme280-pressure":None}

    def __init__(self, requests):
        self.requests = requests
        self.io = IO_HTTP(secrets["aio_username"], secrets["aio_key"], requests)

        for feed in self.feeds:
            self.feeds[feed] = self.setup_feed(feed)

    # Fetch the feed of the provided name. If the feed does not exist, create it.
    def setup_feed(self, feed_name):
        try:
            # Get the feed of provided feed_name from Adafruit IO
            return self.io.get_feed(feed_name)
        except AdafruitIO_RequestError:
            # If no feed of that name exists, create it
            return self.io.create_new_feed(feed_name)


    # Send the data. Requires a feed name and a value to send.
    def send_io_data(self, feed, value):
        return self.io.send_data(feed["key"], value)

    def send_log(self,data):
        try:
            print("Sending data to AdafruitIO...")
            # Send data to Adafruit IO
            self.send_io_data(self.feeds["bme280-temperature"], data["bme280-temperature"])
            self.send_io_data(self.feeds["bme280-temperature-f"], data["bme280-temperature-f"])
            self.send_io_data(self.feeds["bme280-humidity"], data["bme280-humidity"])
            self.send_io_data(self.feeds["bme280-pressure"], data["bme280-pressure"])
            print("Data sent!")
            # Turn off the LED to indicate data sending is complete.
            led.value = False

        # Adafruit IO can fail with multiple errors depending on the situation, so this except is broad.
        except Exception as e:  # pylint: disable=broad-except
            print(e)
            go_to_sleep(60)

        led.off()
        go_to_sleep(sleep_duration)


def print_logged_data():
    print("Current BME280 temperature: {0} C".format(loggedData["bme280-temperature"]))
    print("Current BME280 temperature: {0} F".format(loggedData["bme280-temperature-f"]))
    print("Current BME280 humidity: {0} %".format(loggedData["bme280-humidity"]))
    print("Current BME280 pressure: {0} hPa".format(loggedData["bme280-pressure"]))


def connect_to_wifi():
    try:
        print(f"Connecting to {secrets['ssid']}")
        wifi.radio.connect(secrets['ssid'], secrets['password'])
        print(f"Connected to {secrets['ssid']}")
        print(f"My IP address: {wifi.radio.ipv4_address}")
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        return requests
    except:
        go_to_sleep(60)
        connect_to_wifi()

def go_to_sleep(sleep_period):
    print(f"Going into deep sleep for {sleep_period} seconds...")

    # Turn off I2C power by setting it to input
    i2c_power = digitalio.DigitalInOut(board.I2C_POWER)
    i2c_power.switch_to_input()

    # Create a an alarm that will trigger sleep_period number of seconds from now.
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + sleep_period)
    # Exit and deep sleep until the alarm wakes us.
    alarm.exit_and_deep_sleep_until_alarms(time_alarm)



#connect to the wifi in settings.toml
requests = connect_to_wifi()

aio = IOConnection(requests)

# Turn on the LED to indicate data is being sent.
led.on()

# Print data values to the serial console. Not necessary for Adafruit IO.
print_logged_data()
aio.send_log(loggedData)


