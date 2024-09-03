from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from ..utils.logger import get_logger


logger = get_logger()


class BrowserService:
    def __init__(self, headless=True, window_size="1920,1080", options=None):
        self.driver = None
        self.headless = headless
        self.window_size = window_size
        self.options = options or Options()
        self._initialize_options()

    def _initialize_options(self):
        self.options.add_argument(f'--window-size={self.window_size}')
        if self.headless:
            self.options.add_argument('--headless=new')
        self.options.add_argument('--disable-web-security')
        self.options.add_argument(
            '--disable-features=IsolateOrigins,site-per-process')
        self.options.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--mute-audio')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        logger.info("Browser options initialized")

    def initialize_browser(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service, options=self.options)
            logger.info("Browser initialized")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    def stop_browser(self):
        if self.driver:
            self.driver.stop_client()
            logger.info("Browser client stopped")

    def quit_browser(self):
        if self.driver:
            self.driver.quit()
            logger.info("Browser quit successfully")

    def take_screenshot(self, file_path):
        try:
            if self.driver:
                self.driver.save_screenshot(file_path)
                logger.info(f"Screenshot saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise

    def navigate_to_url(self, url):
        try:
            if self.driver:
                self.driver.get(url)
                logger.info(f"Navigated to {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    def find_element(self, by: By, value: str, timeout=30):
        try:
            if self.driver:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value)))
                logger.info(f"Element found: {value}")
                return element
        except Exception as e:
            logger.error(f"Failed to find element: {value} - {e}")
            raise

    def click_element(self, by: By, value: str, timeout=30):
        try:
            element = self.find_element(by, value, timeout)
            element.click()
            logger.info(f"Clicked element: {value}")
        except Exception as e:
            logger.error(f"Failed to click element: {value} - {e}")
            raise

    def input_text(self, by: By, value: str, text: str, timeout=30):
        try:
            element = self.find_element(by, value, timeout)
            element.send_keys(text)
            logger.info(f"Input text '{text}' into element: {value}")
        except Exception as e:
            logger.error(f"Failed to input text into element: {value} - {e}")
            raise

    def wait_for_url_change(self, current_url, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_changes(current_url))
            logger.info("URL changed successfully")
        except Exception as e:
            logger.error(f"URL did not change within the timeout period: {e}")
            raise

    def get_cookies(self):
        try:
            if self.driver:
                cookies = self.driver.get_cookies()
                logger.info("Cookies retrieved successfully")
                return cookies
        except Exception as e:
            logger.error(f"Failed to get cookies: {e}")
            raise
