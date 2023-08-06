from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options


class AppiumController:
    __drivers = {}
    __driver = None
    bi = BuiltIn()

    def __init__(self):
        pass

    @staticmethod
    def open_application(server_url, alias, desired_caps_dict: dict) -> WebDriver:
        AppiumController.__driver = webdriver.Remote(str(server_url), desired_caps_dict)
        AppiumController.__drivers[alias] = AppiumController.__driver
        return AppiumController.__driver

    @staticmethod
    def open_browser(alias, data_dir, browser='Chrome', is_headless=False):
        if browser.lower() == 'chrome':
            chrome_options = Options()
            if is_headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-data-dir={}".format(data_dir))
            mobile_emulation = {"deviceName": "Nexus 5"}
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            AppiumController.__driver = wd.Chrome(chrome_options=chrome_options)
            AppiumController.__drivers[alias] = AppiumController.__driver
            AppiumController.__driver.maximize_window()

    @staticmethod
    def switch_application(alias):
        all_sessions = AppiumController.get_all_sessions()
        AppiumController.__driver = all_sessions[alias]

    @staticmethod
    def get_session_instance() -> WebDriver:
        if not AppiumController.__driver:
            raise Exception('no application is open')
        return AppiumController.__driver

    @staticmethod
    def get_all_sessions() -> dict:
        return AppiumController.__drivers

    @staticmethod
    def close_session(alias):
        AppiumController.__driver = AppiumController.__drivers[alias]
        AppiumController.__driver.quit()

    @staticmethod
    def close_all_sessions():
        for session in AppiumController.__drivers:
            AppiumController.__drivers[session].quit()
