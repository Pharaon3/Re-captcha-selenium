import datetime
import time
import sys

if sys.platform == 'win32':
    from fctcore import (
        Parser,
        ParseResult,
        check_exists_by_xpath,
        fctselenuim,
        parse_field,
        preg_repace,
    )

else:
    from crawler.fctcore import (
        Parser,
        ParseResult,
        check_exists_by_xpath,
        fctselenuim,
        parse_field,
        preg_repace,
    )



class Test_browser(Parser):
    def __init__(self, use_proxy=False, proxy_list=None):
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list
        self.driver = None
        self.fctbrowser = fctselenuim(
            type="chrome", use_proxy=self.use_proxy, proxy=self.proxy_list
        )  # mobile, chrome, firefox
        self.base_url = 'https://browserleaks.com/ssl'

    def parse_site(
            self,
            firstname: str,
            lastname: str,
            address: str,
            city: str,
            state: str,
            zip: str,
            dob: str,
    ) -> ParseResult | None:
        return None

    def test(self):
        image_name = f'/app/cache/tls-{str(datetime.datetime.now().time())[:8].replace(":", "-")}.png'
        self.fctbrowser.open()
        self.fctbrowser.get(self.base_url, delay=10)
        self.fctbrowser.driver.execute_script("document.body.style.zoom = '70%'")
        self.fctbrowser.driver.execute_script("window.scrollTo(0, window.innerHeight / 3);")
        self.fctbrowser.driver.save_screenshot(image_name)
        self.fctbrowser.close()

if __name__ == '__main__':
    Test_browser(True, ["user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000"]).test()

