Selenium / SeleniumBase (is not connection proxies )
Playwright (browser problem )
Pupputeer / extra stealth (not updated recently 2022 )

PerimeterX
Bypass perimeterx 


from selenium.webdriver import ChromeOptions
from seleniumbase import BaseCase
class AuthProxyTest(BaseCase):
    def test_with_auth_proxy(self):
        # Set proxy and credentials
        proxy = "brd.superproxy.io:33335"
        username = "brd-customer-hl_97d61f65-zone-cityproxy"
        password = "dc1p9n86drhw"
        # Setup Chrome options
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f' - proxy-server={proxy}')
        # Bypass proxy authentication using a Chrome extension
        chrome_options.add_extension('proxy_auth_plugin.zip')
        # Open browser with options
        self.driver = self.get_new_driver(chrome_options=chrome_options)
        self.open("http://example.com")
        # Check some condition
        self.assert_title("Example Domain")
