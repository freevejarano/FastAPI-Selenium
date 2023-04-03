from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set default wait time for elements to be located
lower = 2

class WebPage:

    def __init__(self, url):
        # Intialize driver
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()

        # Initialize main attrs
        self.reason = []
        self.valid = True

        # Access to url and check if it works
        try:
            self.driver.get(url)
            self.url = url
            time.sleep(lower)
        except:
            self.valid = False
            self.reason.append("Wrong page")
            print("URL malformed")


    def make_tests(self):
        # Only if it is wrong page the script stop
        if not self.correct_webpage():
            self.driver.quit()
            return None

        self.translate()
        self.resolution()
        self.javascript()

        self.driver.quit()

    def correct_webpage(self):
        try:
            elements = []
            # index
            logo = self.driver.find_element(By.XPATH, '//a[@data-track-click="nav_click"]')
            elements.append(logo)

            search_bar = self.driver.find_element(By.XPATH, '//form[@action="https://www.classcentral.com/search"]/input')
            elements.append(search_bar)

            assert all(elements), "Wrong page"

        except:
            self.valid = False
            self.reason.append("Wrong page")

        return self.valid

    def translate(self):
        try:
            elements = []

            # check report page
            self.driver.find_element(By.XPATH, '//div[@data-menu="report"]/a').click()

            try:
                simple_h1 = self.driver.find_element(By.XPATH, '//h1[text()="News & Analysis"]')
                simple_h1 = None
            except:
                simple_h1 = "Y"

            elements.append(simple_h1)

            self.driver.execute_script('window.history.go(-1)')

            assert all(elements), "Inner pages are not translated"
        except:
            self.valid = False
            self.reason.append("Inner pages are not translated")

    def javascript(self):
        try:
            # Move the cursor to element to show if it works
            drop_down = self.driver.find_element(By.XPATH, '//div[@data-name="NAV_DROPDOWN"]')
            hover = ActionChains(self.driver).move_to_element(drop_down)
            hover.perform()

            self.driver.find_element(By.XPATH, '//div[@data-menu-dropdown="report"]/div/div/a').click()

            self.driver.execute_script('window.history.go(-1)')
        except:
            self.valid = False
            self.reason.append("Javascript dropdown not working properly")

    def resolution(self):
        try:
            # find a blur in url
            image = self.driver.find_element(By.XPATH, '//main/section/div/img')

            src = image.get_attribute("src")

            assert not "blur" in src, "Images not high resolution"
        except:
            self.valid = False
            self.reason.append("Images not high resolution")