#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GdkPixbuf
import cairo

import random
import math
import os
from time import sleep, time

# time between each sensor mesearuement (1s)
TIME_UPATE = 2000


class Sensors():
    def __init__(self):
        ''' '''
        self.sensor_dictionnary = {}

    def found_iio_device_with_name(self, data, name):
        prefix = "/sys/bus/iio/devices/"
        of_name = 'OF_NAME=' + name
        try:
            for filefolder in os.listdir(prefix):
                with open(prefix + '/' + filefolder + '/uevent') as f:
                    for line in f:
                        if line.split('\n')[0] == of_name:
                            ''' return directory which contains "data" '''
                            if os.path.exists(prefix + '/' + filefolder + '/' + data):
                                return (prefix + '/' + filefolder + '/')
        except OSError:
            pass
        except Exception as exc:
            pass
        return None

    def found_all_sensor_path(self):
        self.sensor_dictionnary['temperature'] = self.found_iio_device_with_name("in_temp_raw", "hts221")
        self.sensor_dictionnary['humidity']    = self.found_iio_device_with_name("in_humidityrelative_raw", "hts221")

        self.sensor_dictionnary['accelerometer'] = self.found_iio_device_with_name("in_accel_x_raw", "lis2dw12")
        if self.sensor_dictionnary['accelerometer'] is None:
            self.sensor_dictionnary['accelerometer'] = self.found_iio_device_with_name("in_accel_x_raw", "lsm6dso")

        self.sensor_dictionnary['magnetometer'] = self.found_iio_device_with_name("in_magn_x_raw", "lis2mdl")
        if self.sensor_dictionnary['magnetometer'] is None:
            self.sensor_dictionnary['magnetometer'] = self.found_iio_device_with_name("in_magn_x_raw", "lsm6dso")

        print("[DEBUG] temperature   -> ", self.sensor_dictionnary['temperature'], "<")
        print("[DEBUG] humidity      -> ", self.sensor_dictionnary['humidity'], "<")
        print("[DEBUG] accelerometer -> ", self.sensor_dictionnary['accelerometer'], "<")
        print("[DEBUG] magnetometer     -> ", self.sensor_dictionnary['magnetometer'], "<")

    def temperature_read(self):
        prefix_path = self.sensor_dictionnary['temperature']
        try:
            with open(prefix_path + "in_temp_" + 'raw', 'r') as f:
                raw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_temp_" + 'raw', exc)
            raw = 0.0
        try:
            with open(prefix_path + "in_temp_" + 'scale', 'r') as f:
                scale = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_temp_" + 'scale', exc)
            scale = 0.0
        try:
            with open(prefix_path + "in_temp_" + 'offset', 'r') as f:
                offset = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_temp_" + 'offset', exc)
            offset = 0.0
        return (offset + raw) * scale

    def humidity_read(self):
        prefix_path = self.sensor_dictionnary['humidity']
        try:
            with open(prefix_path + "in_humidityrelative_" + 'raw', 'r') as f:
                raw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_humidityrelative_" + 'raw', exc)
            raw = 0.0
        try:
            with open(prefix_path + "in_humidityrelative_" + 'scale', 'r') as f:
                scale = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_humidityrelative_" + 'scale', exc)
            scale = 0.0
        try:
            with open(prefix_path + "in_humidityrelative_" + 'offset', 'r') as f:
                offset = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_humidityrelative_" + 'offset', exc)
            offset = 0.0
        return (offset + raw) * scale

    def accelerometer_read(self):
        prefix_path = self.sensor_dictionnary['accelerometer']
        try:
            with open(prefix_path + "in_accel_x_" + 'scale', 'r') as f:
                rscale = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_accel_x_" + 'scale', exc)
            rscale = 0.0

        try:
            with open(prefix_path + "in_accel_" + 'x_raw', 'r') as f:
                xraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_accel_" + 'x_raw', exc)
            xraw = 0.0

        accel_x = int(xraw * rscale * 256.0 / 9.81)
        try:
            with open(prefix_path + "in_accel_" + 'y_raw', 'r') as f:
                yraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_accel_" + 'y_raw', exc)
            yraw = 0.0

        accel_y = int(yraw * rscale * 256.0 / 9.81)
        try:
            with open(prefix_path + "in_accel_" + 'z_raw', 'r') as f:
                zraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_accel_" + 'z_raw', exc)
            zraw = 0.0

        accel_z = int(zraw * rscale * 256.0 / 9.81)
        return [ accel_x, accel_y, accel_z]

    def magnetometer_read(self):
        prefix_path = self.sensor_dictionnary['magnetometer']
        try:
            with open(prefix_path + "in_magn_x_" + 'scale', 'r') as f:
                rscale = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_magn_x_" + 'scale', exc)
            rscale = 0.0
        try:
            with open(prefix_path + "in_magn_" + 'x_raw', 'r') as f:
                xraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_magn_" + 'x_raw', exc)
            xraw = 0.0

        magn_x = int(xraw * rscale * 1000)
        try:
            with open(prefix_path + "in_magn_" + 'y_raw', 'r') as f:
                yraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_magn_" + 'y_raw', exc)
            yraw = 0.0
        magn_y = int(yraw * rscale * 1000)
        try:
            with open(prefix_path + "in_magn_" + 'z_raw', 'r') as f:
                zraw = float(f.read())
        except Exception as exc:
            print("[ERROR] read %s " % prefix_path + "in_magn_" + 'z_raw', exc)
            zraw = 0.0
        magn_z = int(zraw * rscale * 1000)
        return [ magn_x, magn_y, magn_z]

# -------------------------------------------------------------------
# -------------------------------------------------------------------
class MainUIWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Sensor usage")
        #self.set_decorated(False)
        self.maximize()
        self.screen_width = self.get_screen().get_width()
        self.screen_height = self.get_screen().get_height()

        self.set_default_size(self.screen_width, self.screen_height)
        print("[DEBUG] screen size: %dx%d" % (self.screen_width, self.screen_height))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('destroy', Gtk.main_quit)

        # search sensor interface
        self.sensors = Sensors()
        self.sensors.found_all_sensor_path()

        sensor_box = Gtk.VBox(homogeneous=False, spacing=0)

        # temperature
        temp_label = Gtk.Label()
        temp_label.set_markup("<span font_desc='LiberationSans 25'>Temperature</span>")
        self.temp_value_label = Gtk.Label()
        self.temp_value_label.set_markup("<span font_desc='LiberationSans 25'>--.-- °C</span>")
        temp_box = Gtk.HBox(homogeneous=False, spacing=0)
        temp_box.add(temp_label)
        temp_box.add(self.temp_value_label)
        sensor_box.add(temp_box)

        # humidity
        humidity_label = Gtk.Label()
        humidity_label.set_markup("<span font_desc='LiberationSans 25'>Humidity</span>")
        self.humidity_value_label = Gtk.Label()
        self.humidity_value_label.set_markup("<span font_desc='LiberationSans 25'>--.-- %c</span>" % '%')
        humidity_box = Gtk.HBox(homogeneous=False, spacing=0)
        humidity_box.add(humidity_label)
        humidity_box.add(self.humidity_value_label)
        sensor_box.add(humidity_box)

        # Accel
        # Accelerometer is removed since the latency when reading the registers makes the python script misbehave - to be investigated
#        accel_label = Gtk.Label()
#        accel_label.set_markup("<span font_desc='LiberationSans 25'>Accelerometer</span>")
#        self.accel_value_label = Gtk.Label()
#        self.accel_value_label.set_markup("<span font_desc='LiberationSans 25'> [ --.--, --.--, --.--]</span>")
#        accel_box = Gtk.HBox(homogeneous=False, spacing=0)
#        accel_box.add(accel_label)
#        accel_box.add(self.accel_value_label)
#        sensor_box.add(accel_box)

        # Magnetometer
        magn_label = Gtk.Label()
        magn_label.set_markup("<span font_desc='LiberationSans 25'>Magnetometer</span>")
        self.magn_value_label = Gtk.Label()
        self.magn_value_label.set_markup("<span font_desc='LiberationSans 25'> [ --.--, --.--, --.--]</span>")
        magn_box = Gtk.HBox(homogeneous=False, spacing=0)
        magn_box.add(magn_label)
        magn_box.add(self.magn_value_label)
        sensor_box.add(magn_box)

        self.add(sensor_box)

        # Add a timer callback to update
        # this takes 2 args: (how often to update in millisec, the method to run)
        GLib.timeout_add(TIME_UPATE, self.update_ui)


    def destroy(self, widget, data=None):
        Gtk.main_quit()


    def update_ui(self):
        # temperature
        temp = self.sensors.temperature_read()
        self.temp_value_label.set_markup("<span font_desc='LiberationSans 25'>%.02f °C</span>" % temp)
        # humidity
        hum = self.sensors.humidity_read()
        self.humidity_value_label.set_markup("<span font_desc='LiberationSans 25'>%.02f %c</span>" % (hum, '%'))
        # accel
        # accel = self.sensors.accelerometer_read()
        # self.accel_value_label.set_markup("<span font_desc='LiberationSans 25'>[ %.02f, %.02f, %.02f]</span>" % (accel[0], accel[1], accel[2]))
        # magn
        magn = self.sensors.magnetometer_read()
        self.magn_value_label.set_markup("<span font_desc='LiberationSans 25'>[ %d mG, %d mG, %d mG]</span>" % (magn[0], magn[1], magn[2]))

        # As this is a timeout function, return True so that it
        # continues to get called
        return True


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Main
if __name__ == "__main__":
    # add signal to catch CRTL+C
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    win = MainUIWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()

    Gtk.main()

