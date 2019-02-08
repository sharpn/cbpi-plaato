# -*- coding: utf-8 -*-
import urllib2

from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property
import json

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
    refresh_time = Property.Text(
        "Refresh Time", default_value="5", configurable=True)

    def get_unit(self):
        if self.pin == "Temperature":
            return self.get("v108")
        elif self.pin == "Volume":
            return self.get("v109")
        elif self.pin == "Bubbles per minute":
            return "bpm"
        elif self.pin == "ABV":
            return "%"
        else:
            return ""

    def execute(self):
        while self.is_running():
            pin_value = PINS[self.pin]
            refresh = float(self.refresh_time)
            response = self.get(pin_value)

            self.data_received(response)
            self.api.socketio.sleep(refresh)

    def get(self, pin):
        url = "{0}/{1}/get/{2}".format(plaato_base_url, self.api_key, pin)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, error:
            err = error.read()
            print err
        else:
            content = response.read()
            j = json.loads(content)

            if type(j) == list:
                return j[0]
            else:
                return j
