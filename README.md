# fluffy-octo-adventure
esp8266 D1 mini temperature measuring

Measuring temperature from an DS18B20 using an arduino (esp8266 D1 mini) and sending data to a server that gathers data into a database and with help of Grafana builds a nice graph showing the values.

Things needed:
Arduino with wifi capabilities (WeMos D1 mini)
Server with python and Grafana installed (VPS) and a public IP address that is accessable.
DS18B20 sensor

Server Side:
Put server.py and watchdog.py into your /usr/sbin/ folder and make executeable (chmod +x)
Install mysql (mariadb), python and grafana (with all needed dependancies)
edit server.py to your server settings.
