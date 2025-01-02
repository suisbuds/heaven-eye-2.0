import os
import subprocess

subprocess.run(["pyside6-rcc", "resources.qrc", "-o", "resources_rc.py"], check=True)

subprocess.run(["pyside6-uic", "home.ui", "-o", "ui/home.py"], check=True)

subprocess.run(["python3", "main.py"], check=True)