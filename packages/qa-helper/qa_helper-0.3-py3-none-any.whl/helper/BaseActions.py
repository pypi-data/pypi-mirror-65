import os
import random
import re
from copy import copy
from pathlib import Path
from time import sleep

import numpy
from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from deprecated import deprecated
from persiantools import digits
from robot.libraries.BuiltIn import BuiltIn
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from unidecode import unidecode

from Resources.helper.AppiumController import AppiumController
from Resources.helper.XmlElement import XmlFinder, XmlElement
from Variables.passenger_elements_fa import toast_message


class BaseActions:
    """Base Actions class that is initialized on every page object class."""

    def __init__(self):
        self._strategies = {'id': By.ID, 'name': By.NAME,
                            'xpath': By.XPATH,
                            'class': By.CLASS_NAME,
                            'link': By.LINK_TEXT}
        self.bi = BuiltIn()
        self.numpy_agent = numpy

    @staticmethod
    def get_driver_instance():
        return AppiumController.get_session_instance()

    def find(self, locator: dict, timeout=1, page_src=None):
        locator = copy(locator)
        if isinstance(locator, dict):
            if 'xml' in locator and locator['xml']:
                return XmlFinder.find(locator=locator, page_src=page_src, timeout=timeout)
            else:
                driver = self.get_driver_instance()
                driver.implicitly_wait(timeout)
                element = driver
                for prefix in locator:
                    if prefix == 'xml':
                        continue
                    value = locator[prefix]
                    if prefix == 'text':
                        value = "//*[@text='{}']".format(value)
                        prefix = 'xpath'
                    strategy = self._strategies[prefix]
                    try:
                        element = element.find_element(strategy, value)
                    except Exception as e:
                        raise Exception('{} not found with {} strategy'.format(value, strategy))
                driver.implicitly_wait(1)
                return element
        else:
            raise Exception('locator {} is not dictionary'.format(str(locator)))

    def finds(self, locator: dict, page_src=None, timeout=1) -> list:
        locator = copy(locator)
        if 'xml' in locator and locator['xml']:
            return XmlFinder.finds(locator=locator, page_src=page_src, timeout=timeout)
        else:
            driver = self.get_driver_instance()
            driver.implicitly_wait(timeout)
            element = driver
            for prefix in locator:
                if prefix == 'xml':
                    continue
                value = locator[prefix]
                if prefix == 'text':
                    value = "//*[@text='{}']".format(value)
                    prefix = 'xpath'
                strategy = self._strategies[prefix]
                element = element.find_elements(strategy, value)
            driver.implicitly_wait(1)
            return element

    @deprecated(version='new design', reason="This method is deprecated please use find() instead that")
    def wait_for_page_contains_element(self, locator, time_out=5):
        try:
            self.find(locator=locator, timeout=time_out)
        except TimeoutException:
            raise Exception('Not able to find Element:' + locator)

    def get_text(self, locator):
        element = self.find(locator, timeout=5)
        return element.get_attribute("text")

    def wait_for_page_not_contains_element(self, locator, time_out=5):
        for i in range(time_out):
            try:
                self.find(locator)
                sleep(1)
            except:
                return
        raise Exception("Element {} did not disappear in {}".format(locator, str(time_out)))

    @deprecated(version='new design', reason="This method is deprecated please use find_text() instead that")
    def wait_for_page_contains_text(self, text, exact=False, timeout=5):
        if exact:
            locator = {'xpath': "//*[@text='{}']".format(text)}
        else:
            locator = {'xpath': "//*[contains(@text,'{}')]".format(text)}
        self.find(locator, timeout)

    def find_text(self, text, exact=False, timeout=1) -> WebElement:
        if exact:
            locator = {'xpath': "//*[@text='{}']".format(text)}
        else:
            locator = {'xpath': "//*[contains(@text,'{}')]".format(text)}

        return self.find(locator=locator, timeout=timeout)

    def get_elements_count(self, locator):
        return len(self.finds(locator=locator))

    def long_press(self, locator, page_src=None, duration=3000):
        if 'xml' in locator and locator['xml']:
            XmlFinder.find(locator, page_src).long_press(duration)
        else:
            driver = AppiumController.get_session_instance()
            element = self.find(locator)
            action = TouchAction(driver)
            action.press(element).wait(duration).release().perform()

    def long_press_by_element(self, element, duration=3000):
        if isinstance(element, XmlElement):
            element.long_press(duration)
        else:
            driver = self.get_driver_instance()
            action = TouchAction(driver)
            action.press(element).wait(duration).release().perform()

    def wait_until_element_has_attribute(self, locator, attr, attr_status, timeout=5):
        for i in range(timeout):
            try:
                status = self.find(locator).get_attribute(attr)
                if self.to_boolean(status) == attr_status:
                    return True
            finally:
                sleep(1)

        raise Exception('Element not found or element has not attribute {}'.format(str(attr_status)))

    def scroll_to_find_text(self, origin_locator, destination_locator, text, max_scroll=10):
        element = None
        try:
            self.find_text(text=text, timeout=2)
        except:
            origin_center = self.get_center_coordinate(origin_locator)
            destination_center = self.get_center_coordinate(destination_locator)
            while not element:
                if not max_scroll:
                    raise Exception('Cannot find scroll destination')
                driver = self.get_driver_instance()
                try:
                    element = self.find_text(text=text, timeout=2).is_displayed()
                except:
                    driver.swipe(start_x=int(origin_center['x']), start_y=int(origin_center['y']),
                                 end_x=int(destination_center['x']), end_y=int(destination_center['y']))
                    max_scroll = max_scroll - 1

    def scroll_to_find_element(self, origin_locator, destination_locator, target_locator, max_scroll=10):
        element = None
        try:
            self.find(locator=target_locator, timeout=2)
        except:
            origin_center = self.get_center_coordinate(origin_locator)
            destination_center = self.get_center_coordinate(destination_locator)
            while not element:
                if not max_scroll:
                    raise Exception('Cannot find scroll destination')
                driver = self.get_driver_instance()
                try:
                    element = self.find(locator=target_locator, timeout=2)
                except:
                    driver.swipe(start_x=int(origin_center['x']), start_y=int(origin_center['y']),
                                 end_x=int(destination_center['x']), end_y=int(destination_center['y']))
                    max_scroll = max_scroll - 1

    def check_toast_message(self, message=None, timeout=5):
        toast_element = self.find(toast_message, timeout)
        if message:
            assert message in toast_element.text, 'toast message is not {}'.format(message)

    def click_device_back_button(self):
        driver = self.get_driver_instance()
        driver.press_keycode(4)

    @staticmethod
    def to_boolean(string):
        return string.lower() in ['true', 't', '1']

    @staticmethod
    def get_project_root() -> Path:
        """Returns project root folder."""
        return Path(__file__).parent.parent.parent

    @staticmethod
    def convert_persian_number_to_english(number):
        return unidecode(str(number).replace('٬', '').replace(',', ''))

    @staticmethod
    def convert_english_number_to_persian(number):
        return digits.en_to_fa(str(number).replace('٬', '').replace(',', ''))

    @staticmethod
    def get_device_ip(udid):
        cmd = 'adb -s {}'.format(udid) + " shell ip route | awk '{print $9}'"
        return os.popen(cmd).read().replace('\n', '')

    def get_center_coordinate(self, locator):
        bounds = self.find(locator, timeout=3).get_attribute('bounds')
        return BaseActions.calculate_center_of_bounds(bounds)

    @staticmethod
    def calculate_center_of_bounds(bounds):
        result = {}
        bounds = bounds.replace('[', '').replace(']', ',').split(',')
        result.update({'x': (float(bounds[0]) + float(bounds[2])) / 2})
        result.update({'y': (float(bounds[1]) + float(bounds[3])) / 2})
        return result

    def swipe_by_percentage(self, start_x_per, start_y_per, end_x_per, end_y_per, on_map=False):
        """
        Usage :
        swipe_by_percentage(20, 80, 20 , 60)
        This means start swiping from 20% of width and 80% of height and ends on
        20% of width and 60% of height. (Down to Top)
        swipe_by_percentage(20, 50, 60 , 50) # Left to Right
        swipe_by_percentage(60, 80, 20 , 30) # Right to Left
        swipe_by_percentage(30, 40, 30 , 60) # Up to Down
        """
        driver = self.get_driver_instance()
        device_size = driver.get_window_size()
        x_cent = int(device_size['width']) / 100
        y_cent = int(device_size['height']) / 100
        start_x = x_cent * start_x_per
        start_y = y_cent * start_y_per
        end_x = x_cent * end_x_per
        end_y = y_cent * end_y_per
        if on_map:
            driver.swipe(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)
        else:
            driver.flick(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)