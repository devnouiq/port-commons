from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium import webdriver
from .aws import AWSService


class BrowserService:
    def __init__(self, aws_service: AWSService, bucket_name, logger, headless=True, window_size="1920,1080", timeout=60, options=None):
        self.driver = None
        self.aws_service = aws_service
        self.bucket_name = bucket_name
        self.logger = logger  # Use the passed logger instance
        self.run_id = logger.run_id  # Access run_id directly from logger instance
        self.headless = headless
        self.window_size = window_size
        self.timeout = timeout
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
        self.logger.info("Browser options initialized")

    def initialize_browser(self):
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(
                service=service, options=self.options)
            # Set implicit wait for general use
            self.driver.implicitly_wait(self.timeout)
            self.logger.info(
                f"Browser initialized with a timeout of {self.timeout} seconds")
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            raise

    def stop_browser(self):
        if self.driver:
            self.driver.stop_client()
            self.logger.info("Browser client stopped")

    def quit_browser(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser quit successfully")

    def take_screenshot(self, step_name):
        try:
            if self.driver:
                file_path = f'screenshot_{step_name}.png'
                self.driver.save_screenshot(file_path)
                self.logger.info(f"Screenshot saved to {file_path}")

                # Upload the screenshot to S3 using the pre-configured bucket name
                self.aws_service.upload_screenshot(
                    file_path, self.run_id, step_name, self.bucket_name)

                # Clean up local file
                os.remove(file_path)
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            raise

    def navigate_to_url(self, url):
        try:
            if self.driver:
                self.driver.get(url)
                self.logger.info(f"Navigated to {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            raise

    def find_element(self, by: By, value: str):
        try:
            if self.driver:
                element = self.driver.find_element(by, value)
                self.logger.info(f"Element found: {value}")
                return element
        except Exception as e:
            self.logger.error(f"Failed to find element: {value} - {e}")
            raise

    def click_element(self, by: By, value: str, timeout=None):
        try:
            if timeout is None:
                timeout = self.timeout
            self.logger.info(
                f"Waiting for element to be clickable: {value} for up to {timeout} seconds")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value)))
            element.click()
            self.logger.info(f"Clicked element: {value}")
        except Exception as e:
            self.logger.error(f"Failed to click element: {value} - {e}")
            raise

    def input_text(self, by: By, value: str, text: str, timeout=None):
        try:
            if timeout is None:
                timeout = self.timeout
            self.logger.info(
                f"Waiting for element to be visible: {value} for up to {timeout} seconds")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value)))
            element.send_keys(text)
            self.logger.info(f"Input text '{text}' into element: {value}")
        except Exception as e:
            self.logger.error(
                f"Failed to input text into element: {value} - {e}")
            raise

    def wait_for_url_change(self, current_url, timeout=None):
        try:
            if timeout is None:
                timeout = self.timeout
            self.logger.info(
                f"Waiting for URL to change from {current_url} for up to {timeout} seconds")
            WebDriverWait(self.driver, timeout).until(
                EC.url_changes(current_url))
            self.logger.info("URL changed successfully")
        except Exception as e:
            self.logger.error(
                f"URL did not change within the timeout period: {e}")
            raise

    def get_cookies(self):
        try:
            if self.driver:
                cookies = self.driver.get_cookies()
                self.logger.info("Cookies retrieved successfully")
                return cookies
        except Exception as e:
            self.logger.error(f"Failed to get cookies: {e}")
            raise

    # New wait method
    def wait_for_element(self, by: By, value: str, condition="visible", timeout=None):
        try:
            if timeout is None:
                timeout = self.timeout

            self.logger.info(
                f"Waiting for element {value} to become {condition} for up to {timeout} seconds")

            if condition == "visible":
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by, value)))
            elif condition == "clickable":
                WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value)))
            elif condition == "present":
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value)))
            else:
                self.logger.error(f"Invalid wait condition: {condition}")
                raise ValueError("Invalid wait condition")

            self.logger.info(f"Element {value} is {condition} now")
        except Exception as e:
            self.logger.error(
                f"Failed to wait for element {value} to become {condition}: {e}")
            raise

    def execute_script(self, script):
        #Executes JavaScript in the context of maher login page.
        try:
            if self.driver:
                self.logger.info("Executing script")
                result = self.driver.execute_script(script)
                self.logger.info("Script executed successfully")
                return result
        except Exception as e:
            self.logger.error(f"Failed to execute script: {e}")
            raise