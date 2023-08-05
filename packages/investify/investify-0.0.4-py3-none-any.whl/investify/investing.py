import requests
from lxml import html
from requests import RequestException


class Investing:
    def __init__(self, url: str, name: str = None):
        self.url = url
        self.name = name
        self.page = None
        self.ok = None
        self.__user_agent = "InvestingCrawler/1.0"
        self.__headers = {"User-Agent": self.__user_agent}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> str:
        if value:
            self._name = value
        else:
            self._name = self.url.split("/")[-1]
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> str:
        if not value:
            raise ValueError("Value cannot be empty.")
        else:
            self._url = "https://www.investing.com/" + value
        return self._url

    def fetch(self) -> None:
        """Get webpage as defined by url attribute.

        Args:
            None

        Returns:
            page (lxml.htmlElement): Content of the url.

        """
        response = requests.get(self.url, headers=self.__headers)
        self.ok = response.ok

        if response.ok:
            self.page = html.fromstring(response.content)
        else:
            raise RequestException(f"Got {response.status_code}")

    def price(self) -> float:
        """Return the value(price) set by span with @id last_last.

        Args:
            None

        Returns:
            _price (float): Price as present in the span.

        """
        if len(self.page):
            _price_str = str(self.page.xpath("//span[@id='last_last']/text()")[0])
            _price = float(_price_str.replace(",", ""))
            return _price
        else:
            raise ValueError(f"No page found or length of page is {len(self.page)}")
