from urllib.parse import urlencode
import argparse
import json
import pathlib

import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import requests


parser = argparse.ArgumentParser()
parser.add_argument("config", help="JSON: {app:TOKEN,user:TOKEN}")
args = parser.parse_args()

config = json.loads(pathlib.Path(args.config).resolve().read_all())


def handle(_bus, message):
    if message.get_path() != "/org/freedesktop/Notifications":
        return
    (
        app_name,
        _replaces_id,
        _app_icon,
        summary,
        _body,
        _actions,
        _hints,
        _expire_timeout,
    ) = message.get_args_list()
    requests.post(
        "https://api.pushover.net/1/messages.json?{}".format(
            urlencode(
                dict(
                    token=config["token"],
                    user=config["user"],
                    title=app_name,
                    message=summary,
                )
            )
        )
    )


DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_match_string_non_blocking(
    "eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'"
)
bus.add_message_filter(handle)
GLib.MainLoop().run()
