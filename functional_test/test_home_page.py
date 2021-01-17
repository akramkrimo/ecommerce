from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['users.json', 'store.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_failed_signin(self):
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element_by_name('email')
        username_input.send_keys('d.akram13@gmail.com')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('wrong-password')
        self.selenium.find_element_by_xpath('/html/body/div/form/button').click()

        # get the error message
        error_message = self.selenium.find_element_by_name('error_messages').text

        self.assertEqual(
            error_message = 'error: please make sure that you provided the right credentials'
        )

    def test_signin(self):
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element_by_name('email')
        username_input.send_keys('d.akram13@gmail.com')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('akram123')
        self.selenium.find_element_by_xpath('/html/body/div/form/button').click()

        navbar_dropdown = self.selenium.find_element_by_id('navbarDropdown')
        self.assertEquals(
            navbar_dropdown.text, 'Account'
        )

    