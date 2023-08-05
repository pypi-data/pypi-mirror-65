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
import subprocess


class Blink2pngBridge:

    config = {
        "xvfb-run_path": "xvfb-run",
        "execute_path": "blink2png",
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
                self.config[key] = custom_config.get(key)

    def capture(self, url, filename="capture.png"):
        """
        Take snapshot of web page with URL.
        :param url: string
        :param filename: string
        :return:
        """
        xvfb_run = self.config.get("xvfb-run_path")
        execute_path = self.config.get("execute_path")
        save_path = self.config.get("save_path")

        subprocess.Popen([xvfb_run, execute_path, "-o", filename, url], cwd=save_path)
