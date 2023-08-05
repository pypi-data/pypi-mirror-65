# blink2png-bridge  Copyright (C) 2020 Star Inc.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import subprocess


class Blink2pngBridge:
    config = {
        "bridge_timeout": 10,
        "silent": True,
        "xvfb-run_path": "xvfb-run",
        "execute_path": "blink2png",
        "wait": "0",
        "timeout": "10",
        "width": "1024",
        "height": "768",
        "save_path": os.getcwd()
    }

    def __init__(self, custom_config=None):
        """
        Configure custom config if existed.
        :param custom_config: dict
        """
        if custom_config is None:
            custom_config = {}
        for key in custom_config:
            if key in self.config:
                self.config[key] = str(custom_config.get(key))

    def set_wait(self, seconds):
        """
        Set time to wait after loading before the screenshot is taken.
        :param seconds: integer
        :return:
        """
        self.config["wait"] = str(seconds)

    def set_timeout(self, seconds):
        """
        Set time before the request will be canceled.
        :param seconds: integer
        :return:
        """
        self.config["timeout"] = str(seconds)

    def set_save_path(self, path):
        """
        Set save path of snapshots.
        :param path: string (ex. /tmp/snapshot/)
        :return:
        """
        self.config["save_path"] = os.path.join(path)

    def set_window_size(self, width, height):
        """
        Set picture size of snapshots.
        :param width: integer
        :param height: integer
        :return:
        """
        self.config["width"] = str(width)
        self.config["height"] = str(height)

    def save_screenshot(self, url, filename="capture.png"):
        """
        Take snapshot of web page with URL.
        :param url: string
        :param filename: string
        :return:
        """
        save_path = os.path.join(self.config.get("save_path"), filename)

        task = [
            self.config.get("xvfb-run_path"),
            self.config.get("execute_path"),
            "-w", self.config.get("wait"),
            "-t", self.config.get("timeout"),
            "-g", self.config.get("width"), self.config.get("height"),
            "-o", save_path,
            url
        ]

        popen_options = {}
        if self.config.get("silent") is True:
            popen_options["stdout"] = subprocess.PIPE
            popen_options["stderr"] = subprocess.PIPE

        subprocess.Popen(task, **popen_options)

        count, timeout = 0, self.config.get("bridge_timeout")
        while not os.path.isfile(save_path):
            assert count < timeout, "Timeout while checking snapshot existed"
            time.sleep(1)
            count += 1
