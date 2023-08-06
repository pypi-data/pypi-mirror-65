import sys
import random
import datetime
import os
import selenium
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import BrowserManagementKeywords as BM
from SeleniumLibrary import ElementKeywords
from SeleniumLibrary.keywords import WaitingKeywords as WK
from SeleniumLibrary.keywords import *
from json import dumps
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.base import LibraryComponent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from robot.api import logger
from robot.errors import RobotError

class Error(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True

class faciletoolkit(object):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    
    @keyword
    def wait(self, keyword, *keywordargs): 
        """Automatically retries the given keywords/arguments 10 times, each 3 seconds
        """
        BuiltIn().wait_until_keyword_succeeds("10 x", "3 s", keyword, *keywordargs)
 
    @keyword
    def field_returns(self, validity):
        """ Returns DOM error status based on Facile "err wrong" class.
        
            "Validity" set to "invalid" expects the error to pop hence passes the test.
            "Validity" set to "Valid" expects the error to not pop
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary').driver
        source = driver.page_source
        validity = validity.lower()
        if validity == "invalid" and "err wrong" in source:
            logger.info(source)
        elif validity == "invalid" and "err wrong" not in source:
            raise(RobotError("err wrong is in source"))
        elif validity == "valid" and "err wrong" not in source:
            logger.info(source)
        elif validity == "valid" and "err wrong" in source:
            raise(RobotError("source contains 'err wrong' sub-string"))
            
    
    @keyword
    def open_browser(self, url, browser):
        """ Opens the given browser and goes on url.
            browser may be Firefox or Chrome. Firefox may be passed as "ff" aswell.
        """
        browser = browser.lower()
        session = BuiltIn().get_library_instance('SeleniumLibrary')
        if browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            enable_automation = ["enable-automation"]
            chrome_options.add_experimental_option("excludeSwitches", enable_automation)
            session.open_browser(url, browser, options=chrome_options)
        elif browser == "firefox" or "ff":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-gpu")
            firefox_options.add_argument("--disable-extensions")
            session.open_browser(url, browser, options=firefox_options)
        else:
            raise(RobotError("unexpected"))
    
    @keyword
    def open_mobile_browser(self, url, device):
        """ Opens a mobile-emulated chrome session based on the given device and 
            goes to the given url.
        """
        session = BuiltIn().get_library_instance('SeleniumLibrary')
        chrome_options = webdriver.ChromeOptions()
        mobile_emulation = {"deviceName": device}
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        enable_automation = ["enable-automation"]
        chrome_options.add_experimental_option("excludeSwitches", enable_automation)
        session.open_browser(url, "Chrome", options=chrome_options)

    @keyword
    def element_attribute_should_contain_value(self, element, attribute, value):
        """ Returns PASS status if the given element's attribute contains the inputed value.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        attr = driver.get_element_attribute(element, attribute )
        try:
            BuiltIn().should_contain(attr, value)
        except Exception as e:
            raise RobotError(e)

    @keyword
    def element_attribute_should_not_contain_value(self, element, attribute, value):
        """ Returns PASS status if the given element's attribute does not contain the inputed value.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        attr = driver.get_element_attribute(element, attribute )
        try:
            BuiltIn().should_not_contain(attr, value)
        except Exception as e:
            raise RobotError(e)
        
    @keyword
    def clear_session(self):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.delete_all_cookies()
        driver.reload_page()

    @keyword
    def scroll(self, range="0"):
        """ Scrolls the document.

            Ranges might span between 0 to X where 0 is the beginning of the document.

            default is set to 0.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.execute_javascript("document.documentElement.scrollTop = "+range+";")

    @keyword
    def dom_is_loaded(self, timeout="5s"):
        """ returns True if DOM readyState equals "complete" before the given timeout.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.wait_for_condition("return document.readyState=='complete'", timeout)

    @keyword
    def checkpoint(self, locator, timeout="60s"):
        """Waits for a maximum time, defined by timeout argument (default=60s),
           until a webelement (defined by a locator) is contained on the page and displayed
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        faciletoolkit().dom_is_loaded(timeout)
        driver.wait_until_page_contains_element(locator, timeout)
        driver.wait_until_element_is_visible(locator, timeout)
        #da vedere se EC wrappa due condition in una e wrappare i due wait
        log_preventivo = BuiltIn().run_keyword_and_return_status("should_contain", locator, "AS_result_content", None, True, False)
        if log_preventivo:
            faciletoolkit().I_log_id_preventivo()
    
    @keyword
    def I_log_id_preventivo(self):
        """
        checks if the given Id Preventivo is present on the page
        and logs it to a csv file located in the default output folder
        """
        Suite = BuiltIn().get_variable_value("${SUITE_NAME}")
        Test = BuiltIn().get_variable_value("${TEST_NAME}")
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        status, id_preventivo = BuiltIn().run_keyword_and_ignore_error("Execute_javascript", "return AS_Preventivo.ID_PREV")
        logger.console("\nid preventivo: %s" % id_preventivo)
        date = datetime.datetime.now()
        pwd = os.getcwd()
        nome_file = pwd + "/id_preventivi.csv"
        check = os.path.exists(nome_file)
        try:
            if "JavascriptException" not in id_preventivo and check:
                f = open(nome_file, "w+", encoding="UTF-8")
                f.write("{}, {}, {}, {}\n".format(date, Suite, Test, id_preventivo))
                f.close()
            elif "JavascriptException" not in id_preventivo and check == False:
                print("4")
                logger.console("%s not accessible, creating new log file " % nome_file)
                file_preventivo = open(nome_file, "w+", encoding="UTF-8")
                file_preventivo.write("{}, {}, {}, {}\n"
                                    .format(date, Suite, Test, id_preventivo))
                file_preventivo.close()
        except Exception and IOError as e:
            raise Error(status)
                

    @keyword
    def select_from_list_random_index(self, locator, start_index=1):
        """
        Selects a random option from a Select WebElement specified by a locator,
        it is possible to specify a start index for the random selection
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        faciletoolkit().dom_is_loaded()
        element = driver.get_webelement(locator)
        element_id = driver.get_element_attribute(element, "id")
        BuiltIn().run_keyword_and_ignore_error("Checkpoint", "//*[@id='"+element_id+"']//option[string-length(@value)>0]", "10s")
        list_length = driver.execute_javascript("return arguments[0].options.length", "ARGUMENTS",  element)
        logger.info(str(list_length) + " " +  element_id)
        if list_length == 1:
            return "null"
        random_index = random.randint(start_index, list_length-1)
        random_index = str(random_index)
        driver.select_from_list_by_index(locator, random_index)
    
    @keyword
    def select_from_list_random_index_optional(self, *locators):
        """
        Wrapper for "select from list random index" keyword, the random selection
        is performed only if the select element is present on the page
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        for locator in locators:
            lista_presente = BuiltIn().run_keyword_and_return_status("checkpoint", locator, "2s")
            if lista_presente:
                faciletoolkit().select_from_list_random_index(locator)

    @keyword
    def I_land_on_page(self, url, timeout="60s"):
        """
        Waits for a maximum time, defined by timeout argument (default=60s),
        until the location contains a portion of the url (specified by the parameter 'url')
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.wait_for_condition("return document.location.href.includes('%s')" % url, timeout)
        faciletoolkit().dom_is_loaded()

    @keyword
    def javascript_click_TA(self, locator):
        """
        This keyword clicks a WebElement or a locator that represent a WebElement via Javascript
        """
        is_webelement = isinstance(locator, selenium.webdriver.remote.webelement.WebElement)
        if is_webelement:
            faciletoolkit().Javascript_Click_WebElement(locator)
        else:
            faciletoolkit().Javascript_Click_by_Locator(locator)
    
    @keyword
    def Javascript_Click_WebElement(self, element):
        """
        This keyword clicks a WebElement via Javascript
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        driver.execute_javascript("arguments[0].click()", "ARGUMENTS", element)

    @keyword
    def Javascript_Click_by_Locator(self, locator):
        """
        Clicks a locator that represent a WebElement via Javascript
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        element = driver.get_webelement(locator)
        driver.execute_javascript("arguments[0].click()", "ARGUMENTS", element)    

    @keyword
    def check_page_locators(self, *locators):
        """
        Loops over an array of locators and checks
        if the webelements represented by them are visible on the page
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        errors = []
        for i in locators:
            try:
                driver.element_should_be_visible(i)
            except Exception as e:
                errors.append(str(e))
        if len(errors) > 0:
            BuiltIn().fail("\n".join(errors))
    
    @keyword
    def Select_first_autocomplete_option(self):
        """
        Selects the first autocomplete option for auto-complete fields.
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        locator_option = "css:.autocomplete-suggestions:not([style*='display']):not([style*='none']) strong"
        BuiltIn().run_keyword_and_ignore_error("Checkpoint", locator_option, "2s")
        BuiltIn().run_keyword_and_ignore_error("Javascript_click_ta", locator_option)

    @keyword
    def get_right_locator(self, *locators, checkpoint_timeout="200ms"):
        """
        Returns the first locator that exist and is visible
        on the page from a list of locators/WebElements
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        errors = []
        for locator in locators:
            try:
                exists = BuiltIn().run_keyword_and_return_status("Checkpoint", locator, checkpoint_timeout)
                if exists:
                    return locator
            except Exception as e:
                pass
            

    @keyword
    def press_key_on_active_element(self, key):
        """
        Inputs the given key to the active element in DOM
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        active_element = driver.execute_javascript("return document.activeElement;")
        driver.press_keys(active_element, key)
    
    @keyword
    def wait_for_autocomplete_visibility_to_be(self, bool):
        """
        Lets the driver wait until the autocomplete div 
        is visible (True) / hidden (False)
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        locator_autocomplete = "//div[@class='autocomplete-suggestions' and not(contains(@style,'display: none'))]"
        if bool:
            driver.wait_until_page_contains_element(locator_autocomplete)
        else:
            driver.wait_until_page_does_not_contain_element(locator_autocomplete)
    
    @keyword
    def get_text_from_webelements(self, *webelements):
        """
        Takes in input a WebElements array and
        returns a string array containing the stripped texts retrieved from the webelements
        """
        driver = BuiltIn().get_library_instance('SeleniumLibrary')
        text_list = []
        for element in webelements:
            text = driver.get_text(element)
            text = text.strip()
            text_list.append(text)
        return text_list

    @keyword
    def generate_random_number_as_string(self, min, max):
        """
        Generates a random number between the range given by "min", "max" arguments
        and returns it as string
        """
        num = str(random.randint(min, max))
        return num

    @keyword
    def select_random_item_from_list(self, *list):
        """
        Returns a random item from the given list
        """
        item = random.choice(list)
        return item

    @keyword
    def I_click_the_button_prosegui(self):
        """
        This keyword check if "Prosegui" button is present and visible, then clicks it
        """
        button = "id:pulsanteAvanti"
        faciletoolkit().checkpoint(button)
        faciletoolkit().javascript_click_TA(button)

    @keyword
    def check_if_error_message_is_present_on_page(self, message):
        """
        Checks if the given error message is present in DOM
        """
        try:
            faciletoolkit().checkpoint("//span[contains(.,'%s') and contains(@class,'err wrong')]" % message, "5s" )
            logger.info("%s is contained in error message" % message)
        except Exception as e:
            raise Error(e)