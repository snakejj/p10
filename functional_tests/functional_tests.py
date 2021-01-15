from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from purbeurre.settings import BASE_DIR

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
firefox_options.add_argument('--window-size=1920x1080')


class FunctionalTests(StaticLiveServerTestCase):

    # def setUp(self):
    #     cap = DesiredCapabilities().FIREFOX
    #     cap["marionette"] = True
    #     self.driver = webdriver.Firefox(capabilities=cap, executable_path='webdrivers/geckodriver')
    #
    #
    # def tearDown(self):
    #     pass


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox(
            executable_path=str(BASE_DIR / 'webdrivers' / 'geckodriver'),
            options=firefox_options,
        )
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def test_sign_up_process(self):
        self.driver.get(self.live_server_url)
        WebDriverWait(self.driver, 10)

        assert "Page d'accueil" in self.driver.title

        # Go to the login page
        try:
            link_to_login_page = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "login"))
            )
            link_to_login_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.driver.quit()

        # Go to the sign up page
        try:
            link_to_signup_page = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "signup"))
            )

            link_to_signup_page.click()

        except:
            print("The page loading was greater than 10 seconds, hence the test was stopped")
            self.driver.quit()

        # Filling the form

        self.driver.find_element_by_name('username').send_keys('test_username')
        self.driver.find_element_by_name('first_name').send_keys('test_first_name')
        self.driver.find_element_by_name('last_name').send_keys('test_last_name')
        self.driver.find_element_by_name('email').send_keys('test@mail.com')
        self.driver.find_element_by_name('password1').send_keys('password654sq%')
        self.driver.find_element_by_name('password2').send_keys('password654sq%')

        # Submitting the form

        self.driver.find_element_by_id("button_send").click()

        WebDriverWait(self.driver, 10)

        assert "Page de profil" in self.driver.title




