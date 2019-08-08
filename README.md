# ThingWorx IoT Device using balenaCloud

This is a demonstration to show how to connect an sensor on an IoT device (a Raspberry Pi) to ThingWorx using balenaCloud.

## The Components

For this demonstration, I am using these components:

- Raspberry Pi 3 B+ with a MicroSD card
- [Adafruit MCP9808](https://www.adafruit.com/product/1782) I2C temperature sensor
- [balenaCloud](https://www.balena.io/) account (you can sign up for a free account that lets you run 10 devices)
- [PTC ThingWorx Foundation](https://www.ptc.com/en/products/iiot/thingworx-platform) (you can [download a 90 day trial](https://developer.thingworx.com/en/resources/downloads))

### What's balenaCloud?

balenaCloud allows me to manage the the Pi remotely and update everything on the Pi using containers. I can log in to
the console to remotely run diagnostics and monitor the device. If you use Raspberry Pi or other resource-constrained IoT devices,
I highly recommend giving balena a try. It's an excellent platform for managing devices and the team there is doing
a lot of great stuff. 

### What's ThingWorx?

ThingWorx is an Industrial IoT (IIoT) platform that allows rapid development of applications for industrial uses. 
You can quickly create web applications that can interact and display data from disparate systems. In this application,
I'll be pulling data from a web weather source along with the sensor from the Pi. In an production IIoT system,
this could just as easily be data from a machine sensor along with production data from an MES system.

For this example, we are using the Rest API that is built into ThingWorx. For a larger scale system, I'd suggest either
using the ThingWorx Edge SDK or the ThingWorx Edge Microserver.

## The Setup

Clone this repository to your own computer and let's get rolling...

### Hardware

First, you need to wire up the sensor. Per Adafruit's [guide](https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide/python-circuitpython#python-computer-wiring-4-3): 

- Pi 3V3 to sensor VIN
- Pi GND to sensor GND
- Pi SCL to sensor SCK
- Pi SDA to sensor SDA

### balena

1. After you've made an account with balena, log into the dashboard and click "Create application".
2. Type whatever application name that you'd like (mine is "thingworx"), select Raspberry Pi 3 as the device type,
    keep the application type to "Starter", then click "Create new application".
3. Now click on "+ Add device".
4. Keep the device, OS, and edition defaults. If you're using a Wifi connection on the Pi, select "Wifi + Ethernet" and enter in your Wifi credentials.
5. Click "Download balenaOS" and follow the instructions on the right to burn the image and boot the Pi onto balena.
6. After the device appears on the dashboard, look for `git remote add balena` text at the top right of the application view and copy that line.
7. In a command line in this repository directory on your computer, paste that line and run it.
8. balena is all ready!

### ThingWorx

1. After installing ThingWorx, login to the composer.
2. Create a new Thing called "ExampleThing" based on the GenericThing template, and add a number property of "temperature" that is logged.
3. Create a new user (the name is not important -- I called mine "piDataUser") that has no password and is enabled.
4. Create a new application key (again, the name is not important -- I called mine "piKey") with an expiration date somewhere
    in the future and that uses the user you just created.
5. Copy the Key ID that is created for the application key after hitting save, and update the `TWX_APPKEY` varaible in `sensor/scripts/measure_mcp9808.py`.
6. Update the `TWX_SERVER` variable as appropriate in `sensor/scripts/measure_mcp9808.py`.
7. After saving that file, run `git commit sensor/scripts/measure_mcp9808.py` and then `git push balena master`.
    This will run the build scripts on balena and push this container to your Pi. If all is successful, your temperature sensor will now
    be publishing data to the ExampleThing temperature propery.