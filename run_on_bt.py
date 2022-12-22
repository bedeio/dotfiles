#!/usr/bin/env python
# Toggles headset connection

from __future__ import print_function
from __future__ import unicode_literals

# Original solution found here:
# https://askubuntu.com/questions/48001
# /connect-to-bluetooth-device-from-command-line

# Info on dbus packages in python can be found here:
# https://wiki.python.org/moin/DbusExamples

# Required API was discovered initially through reading this page:
# http://www.bluez.org/bluez-5-api-introduction-and-porting-guide/

# I followed this as an example:
# https://github.com/bbirand/python-dbus-gatt/blob/master/devices.py

# This page appears to show all the properties available from bluez
# https://github.com/Azure/iot-edge-v1/blob/master/v1/modules/ble/deps/linux
# /dbus-bluez/xml/org.bluez.Device1.xml

import dbus
from dbus.mainloop.glib import DBusGMainLoop

def find_headset(bus):
  manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                           "org.freedesktop.DBus.ObjectManager")
  objects = manager.GetManagedObjects()

  for path, ifaces in objects.items():
    if ("org.bluez.Device1" in ifaces and
        "org.freedesktop.DBus.Properties" in ifaces):
      iprops = dbus.Interface(
          bus.get_object("org.bluez", path),
          "org.freedesktop.DBus.Properties")
      props = iprops.GetAll("org.bluez.Device1")
      print(props)
      # Note that bluetooth device class 0x240404 = 2360324 = "Headset"
      # Could also match on other properties like "Name". See bluez docs for
      # whats available.
      if props.get("Class") == 0x240404:
        if props.get("Connected"):
          print("Found headset {} ({}) but it is already connected"
                .format(props.get("Name"), props.get("Address")))
          continue
        return path
    return None

def main():
  dbus_loop = DBusGMainLoop()
  bus = dbus.SystemBus(mainloop=dbus_loop)
  hpath = find_headset(bus)

  if hpath:
    adapter = dbus.Interface(
        bus.get_object("org.bluez", hpath), "org.bluez.Device1")
    adapter.Connect()

if __name__ == "__main__":
  main()
