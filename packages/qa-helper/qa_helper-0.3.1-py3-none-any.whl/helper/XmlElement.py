from time import sleep
import xml.etree.ElementTree as ET

from appium.webdriver.common.touch_action import TouchAction

from Resources.helper.AppiumController import AppiumController


class XmlElement(object):
    def __init__(self, page_src, element):
        self.page_src = page_src
        self.element = element

    def get_coordinate_of_element(self):
        bounds = self.element.attrib['bounds']
        from Resources.helper.BaseActions import BaseActions
        return BaseActions.calculate_center_of_bounds(bounds)

    def long_press(self, duration):
        driver = AppiumController.get_session_instance()
        action = TouchAction(driver)
        cord = self.get_coordinate_of_element()
        action.press(x=cord['x'], y=cord['y']).wait(duration).release().perform()

    def click(self):
        self.long_press(duration=1000)

    def get_attribute(self, attribute):
        return self.element.attrib[attribute]

    @staticmethod
    def get_driver_instance():
        return AppiumController.get_session_instance()


class XmlFinder(object):
    @staticmethod
    def get_elements(page_src, attr: dict) -> list:
        result = []
        page_src_xml = ET.fromstring(page_src)
        for element in page_src_xml.iter():
            flag = True
            for item in attr:
                try:
                    if item == 'id':
                        assert attr[item] in element.get('resource-id')
                        continue
                    assert attr[item] in element.get(item)
                except:
                    flag = False
                    break
            if flag:
                result.append(XmlElement(page_src, element))
        return result

    @staticmethod
    def finds(locator, page_src=None, timeout=5) -> list:
        flag = False
        del locator['xml']
        for i in range(timeout * 10):
            if not page_src or flag:
                driver = XmlElement.get_driver_instance()
                page_src = driver.page_source
                flag = True
            elements = XmlFinder.get_elements(page_src=page_src, attr=locator)
            if elements:
                return elements
            else:
                sleep(.1)
        return []

    @staticmethod
    def find(locator, page_src=None, timeout=5) -> XmlElement:
        try:
            return XmlFinder.finds(locator, page_src, timeout)[0]
        except Exception:
            raise Exception('page src has not attributes {}'.format(str(locator)))
