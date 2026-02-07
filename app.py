import json
import os
import subprocess
import sys
import time
from threading import Thread

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, GLib, Notify, Gdk

USER = os.getenv("USER")
BASE_DIR = "/home/waffle/Applications/Open-source/Time guardian"
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USAGE_FILE = os.path.join(DATA_DIR, "usage.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# ensure files exist
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"daily_limit_minutes": 120, "daily_limit_seconds": 0}, f)

if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "w") as f:
        json.dump({"used_minutes": 0, "used_seconds": 0}, f)


def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def notify(message):
    """Send system notification (notify-send)."""
    try:
        subprocess.run(["notify-send", "Time Guardian", message])
    except Exception:
        # fallback logging
        with open(os.path.join(DATA_DIR, "tg.log"), "a") as log:
            log.write(f"{time.ctime()}: {message}\n")


class TimeGuardian:
    def __init__(self):
        usage = load_json(USAGE_FILE, {})
        config = load_json(CONFIG_FILE, {})
        self.used_seconds_total = usage.get("used_minutes", 0) * 60 + usage.get("used_seconds", 0)
        self.limit_seconds_total = config.get("daily_limit_minutes", 0) * 60 + config.get("daily_limit_seconds", 0)
        self.five_minute_warned = False
        self.locked = False

        Notify.init("Time Guardian")
        self.mainloop = GLib.MainLoop()

    def run(self):
        """Main headless timer loop."""
        # Start GTK MainLoop in separate thread
        thread = Thread(target=self.mainloop.run, daemon=True)
        thread.start()

        while True:
            if not self.locked:
                if self.used_seconds_total < self.limit_seconds_total:
                    # increment usage
                    self.used_seconds_total += 1
                    used_minutes = self.used_seconds_total // 60
                    used_seconds = self.used_seconds_total % 60
                    save_json(USAGE_FILE, {"used_minutes": used_minutes, "used_seconds": used_seconds})

                    remaining = max(self.limit_seconds_total - self.used_seconds_total, 0)
                    if remaining == 5 * 60 and not self.five_minute_warned:
                        notify("Only 5 minutes remaining!")
                        self.five_minute_warned = True

                    time.sleep(1)
                else:
                    # time is up → show GTK lockdown UI
                    GLib.idle_add(self.show_lockdown_ui)
                    self.locked = True
            else:
                time.sleep(1)  # wait until unlocked

    def show_lockdown_ui(self):
        """Show fullscreen lock window requiring password."""
        self.dialog = Gtk.Window()
        self.dialog.set_title("Time Guardian Locked")
        self.dialog.set_resizable(False)
        self.dialog.set_decorated(False)
        self.dialog.set_modal(True)
        self.dialog.fullscreen()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)

        label = Gtk.Label(label="Time Guardian has locked your system.\nEnter password to unlock:")
        label.set_wrap(True)

        entry = Gtk.Entry()
        entry.set_visibility(False)
        entry.set_placeholder_text("Password")

        button = Gtk.Button(label="Unlock")

        def check_password(_):
            if entry.get_text() == "8393":
                self.dialog.destroy()
                self.locked = False
                self.used_seconds_total = 0
                save_json(USAGE_FILE, {"used_minutes": 0, "used_seconds": 0})
                self.five_minute_warned = False
            else:
                entry.set_text("")
                label.set_text("Incorrect password. Try again:")

        button.connect("clicked", check_password)
        entry.connect("activate", check_password)

        box.append(label)
        box.append(entry)
        box.append(button)
        self.dialog.set_child(box)
        self.dialog.present()


if __name__ == "__main__":
    tg = TimeGuardian()
    tg.run()
