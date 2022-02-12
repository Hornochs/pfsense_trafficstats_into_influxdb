#!/usr/local/bin/python3.8
import json
import subprocess
from datetime import datetime

from influxdb import InfluxDBClient

INTERFACES = ["igb0", "pppoe0"]
WORKING_FOLDER = "/tmp/json"
NOW = datetime.now()
CLIENT = InfluxDBClient("host", "8086", "user", "pw", "firewall")


# Process an interfaces.X.traffic.PERIOD dict into a pair of (previous_rx, previous_tx), (current_rx, current_tx)
def process_traffic(traffic):
    if len(traffic) != 2:
        return ((0, 0), (traffic[0]["rx"], traffic[0]["tx"]))
    return ((traffic[0]["rx"], traffic[0]["tx"]), (traffic[1]["rx"], traffic[1]["tx"]))


def process_iface(interface):
    day_json = f"{WORKING_FOLDER}/{interface}_d.json"
    month_json = f"{WORKING_FOLDER}/{interface}_m.json"
    # TODO: consider shlex.quote for safety
    subprocess.check_call(
        f"vnstat --json d 2 -i {interface} > {day_json}",
        shell=True,
    )
    subprocess.check_call(
        f"vnstat --json m 2 -i {interface} > {month_json}",
        shell=True,
    )

    with open(day_json, "r") as j:
        day_data = json.loads(j.read())
    with open(month_json, "r") as k:
        month_data = json.loads(k.read())

    (yesterday_rx, yesterday_tx), (today_rx, today_tx) = process_traffic(
        day_data["interfaces"][0]["traffic"]["day"]
    )
    (last_month_rx, last_month_tx), (this_month_rx, this_month_tx) = process_traffic(
        month_data["interfaces"][0]["traffic"]["month"]
    )

    json_body = [
        {
            "measurement": f"stats_{interface}",
            "time": NOW,
            "fields": {
                "yesterday_rx": yesterday_rx,
                "yesterday_tx": yesterday_tx,
                "yesterday_total": int(yesterday_rx) + int(yesterday_tx),
                "today_rx": today_rx,
                "today_tx": today_tx,
                "today_total": int(today_rx) + int(today_tx),
                "last_month_rx": last_month_rx,
                "last_month_tx": last_month_tx,
                "last_month_total": int(last_month_rx) + int(last_month_tx),
                "this_month_rx": this_month_rx,
                "this_month_tx": this_month_tx,
                "this_month_total": int(this_month_rx) + int(this_month_tx),
            },
        }
    ]

    CLIENT.write_points(json_body)


def main():
    for interface in INTERFACES:
        process_iface(interface)

if __name__ == "__main__":
    main()
