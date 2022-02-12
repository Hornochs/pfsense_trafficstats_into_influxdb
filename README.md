# Pythonscript: Pushing interface traffic stats into an influxdb

If you want to have your Trafficstats into an InfluxDB to show it on a grafanaboard, this script will help

## Requirements

 - pfSense 2.5.2 or higher
 - installed influxdb Module on pfsense
 - working influxdb

## Installation

 - If you didn't installed pip on pfsense, do it with `/usr/local/bin/python3.8 -m ensurepip`
 - install influxdb module: `/usr/local/bin/python3.8 -m pip install influxdb`
 - copy `trafficstats.py` into `/usr/local/pythonscripts` (create folder of neccessary)
 - make changes for the interfaces you want to copy (and make sure the working directory exists!)
 - make changes in `CLIENT` constant to build the connection to your influxdb
 - make the script executable: `chmod +x trafficstats.py`

## Huge thanks to [AKX](https://stackoverflow.com/users/51685/akx)
While working on my script, the move to pfSense didn't worked. But he aswered my questions and helped me in [enter link description here](https://stackoverflow.com/a/71090359/13658245). So huge Shoutout to him! Without him it wouldn't be possible!
