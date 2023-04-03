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
        self.base_url = 'https://bot.sannysoft.com/'

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
        self.fctbrowser.open()
        self.fctbrowser.get(self.base_url, delay=5)
        time.sleep(10000)


if __name__ == '__main__':
    Test_browser(True, ["user-maximcrawl:cokeISit@gate.dc.smartproxy.com:20000"]).test()

