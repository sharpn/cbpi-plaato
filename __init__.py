# -*- coding: utf-8 -*-
import urllib2

from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property

PINS = {
    "Bubbles per minute": "v102",
    "Temperature": "v103",
    "Volume": "v104",
    "Original Gravity": "v105",
    "Specific Gravity": "v106",
    "ABV": "v107",
    "Total Bubbles": "v110",
    "Co2": "v119"
}

plaato_base_url = 'http://plaato.blynk.cc'


@cbpi.sensor
class PlaatoSensor(SensorActive):
    pins = []
    for key in PINS.keys():
        pins.append(key)

    api_key = Property.Text("Api Key", configurable=True)
    pin = Property.Select(
        "Pin", options=pins, description="Select which metric you want to listen for")
    unit = Property.Select("Unit", options=["°C", "°F"])
    refresh_time = Property.Text(
        "Refresh Time", default_value="5", configurable=True)

    def get_unit(self):
        return self.unit

    def execute(self):
        while self.is_running():
            pin_value = PINS[self.pin]
            refresh = float(self.refresh_time)
            url = "{0}/{1}/get/{2}".format(
                plaato_base_url, self.api_key, pin_value)
            print(url)
            # contents = urllib2.urlopen(url).read()
            # print(contents)
            self.data_received(2)
            self.api.socketio.sleep(refresh)

        # contents = urllib2.urlopen(url).read()
        # print(contents)
