from os.path import join
from pathlib import Path

from Resources.helper.BaseActions import BaseActions
from Variables.configs import *
import os
from time import sleep, time
from robot.libraries.BuiltIn import BuiltIn
from Resources.helper.AppiumController import AppiumController
from Variables.main_vars import *


class AppAgent:
    def __init__(self, image=image_name):
        self.bi = BuiltIn()
        self.ac = AppiumController()
        self.image = image
        project_root = str(BaseActions.get_project_root())
        self.screen_shots = join(project_root, 'ScreenShots')
        Path(self.screen_shots).mkdir(parents=True, exist_ok=True)

    def switch_application(self, alias: str):
        self.bi.log_to_console('switch to "{}" alias'.format(alias.lower()))
        return self.ac.switch_application(alias.lower())

    def close_all_applications(self, image=None):
        image = image or self.image
        # a = time()
        try:
            self.ac.get_session_instance().save_screenshot(join(self.screen_shots, '{}.png'.format(image)))
            self.bi.log_to_console(join(self.screen_shots, '{}.png'.format(image)))
        except:
            pass
        self.ac.close_all_sessions()

    def get_all_sessions(self):
        return self.ac.get_all_sessions()

    @staticmethod
    def change_gps_status(status, app):
        udid = passenger_device_udid
        st = {'on': '+', 'off': '-'}
        if app.lower() == 'driver':
            udid = driver_device_udid
        os.system(
            "adb -s {} shell settings put secure location_providers_allowed {}gps".format(udid, st[status.lower()]))
        sleep(1)

    def put_app_on_background(self):
        driver = self.ac.get_session_instance()
        driver.close_app()

    def bring_app_to_foreground(self):
        driver = self.ac.get_session_instance()
        driver.launch_app()

    def put_app_on_background_and_open_again(self, duration):
        driver = self.ac.get_session_instance()
        driver.background_app(seconds=duration)

    @staticmethod
    def put_app_on_background_with_home_key():
        driver = AppiumController.get_session_instance()
        driver.press_keycode(3)

    @staticmethod
    def change_device_location(lat, lng):
        driver = BaseActions.get_driver_instance()
        driver.set_location(latitude=lat, longitude=lng)

    @staticmethod
    def close_keyboard():
        driver = BaseActions.get_driver_instance()
        if driver.is_keyboard_shown():
            driver.hide_keyboard()

    @staticmethod
    def get_device_location():
        driver = BaseActions.get_driver_instance()
        return driver.location

    def kill_the_app(self,app):
        apps={'passenger': passenger_app_package, 'driver': driver_app_package}
        driver = self.ac.get_session_instance()
        driver.terminate_app(apps[app])

    @staticmethod
    def device_back_button():
        driver = AppiumController.get_session_instance()
        driver.press_keycode(4)
