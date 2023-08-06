from urllib.parse import urlencode
import argparse
import json
from pathlib import Path

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import requests


parser = argparse.ArgumentParser()
parser.add_argument("config", help="JSON: {app:TOKEN,user:TOKEN}")
args = parser.parse_args()

config = json.loads(Path(args.config).resolve().read_text())
app_token = config["app"]
user_token = config["user"]


def handle(_bus, message):
    if message.get_path() != "/org/freedesktop/Notifications":
        return
    (
        app_name,
        _replaces_id,
        _app_icon,
        summary,
        body,
        _actions,
        _hints,
        _expire_timeout,
    ) = message.get_args_list()
    print("Message: {} / {}: {}".format(app_name, summary, body))
    res = requests.post(
        "https://api.pushover.net/1/messages.json?{}".format(
            urlencode(
                dict(
                    token=app_token,
                    user=user_token,
                    title="{} / {}".format(app_name, summary),
                    message=body,
                )
            )
        )
    )
    if res.status_code > 299:
        print("Send failed with code: {}\n{}".format(res.status_code, res.text))


DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_match_string_non_blocking(
    "eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'"
)
bus.add_message_filter(handle)
GLib.MainLoop().run()
