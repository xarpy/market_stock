import logging
import random
import re

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from server.core.exceptions import ServiceError
from server.core.settings import Settings, settings

logger = logging.getLogger(__name__)


class MarketWatchScraper:
    def __init__(self, skip_browser: bool = False, context: Settings = settings):
        self.data = {}
        self._context = context
        self._link = self._context.MARKETWATCH_URI
        self._headless = skip_browser
        self._headers = {}
        self._user_agent = ""

    def _select_user_agent(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64, rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/123.0.2420.81",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/109.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/109.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]
        self._user_agent = random.choice(user_agent_list)

    def _set_headers(self, symbol: str):
        new_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "letsGetMikey=enabled; refresh=off; mw_loc=%7B%22Region%22%3A%22X%22%2C%22Country%22%3A%22AR%22%2C%22Continent%22%3A%22NA%22%2C%22ApplicablePrivacy%22%3A0%7D; gdprApplies=false; ab_uuid=22442344-6a35-4a17-a90b-a9344bc9461c; fullcss-home=site-6339f8c9e6.min.css; refresh=off; icons-loaded=true; letsGetMikey=enabled; _lr_geo_location_state=PB; _lr_geo_location=BR; fullcss-quote=quote-86ec49efa6.min.css; recentqsmkii=Stock-US-AAPL",
            "Referer": f"https://www.marketwatch.com/investing/stock/{symbol}",
            "Referrer-Policy": "no-referrer-when-downgrade",
        }
        self._headers = new_headers

    def _validate_page_content(self, html):
        if html.find("https://geo.captcha-delivery.com/") == -1:
            raise ServiceError("Bot has found captcha!")

    def run(self, company: str) -> dict:
        try:
            url = "{}/{}".format(self._link, company)
            self._set_headers(company)
            html = self.fetch_data(url)
            self._validate_page_content(html)
            soup = BeautifulSoup(html, "html.parser")
            self.data["company_code"] = company.upper()
            self.data["company_name"] = self.extract_company_name(soup)
            self.data["performance"] = self.extract_performance_data(soup)
            self.data["competitors"] = self.extract_competitors_data(soup)
            return self.data
        except ServiceError as error:
            logger.exception(error)

    def fetch_data(self, url: str) -> str:
        player = sync_playwright().start()
        browser = player.chromium.launch(headless=self._headless)
        context = browser.new_context(user_agent=self._user_agent, extra_http_headers=self._headers)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(15000)
        # page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
        page_content = page.content()
        browser.close()
        return page_content

    def extract_performance_data(self, soup: BeautifulSoup) -> dict:
        table = soup.find("table", class_="table--primary")
        performance_data = {}
        for row in table.find_all("tr", class_="table__row"):
            cells = row.find_all("td", class_="table__cell")
            if len(cells) == 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].find("li", class_="content__item value").get_text(strip=True)
                if label == "5 Day":
                    performance_data["five_days"] = value
                elif label == "1 Month":
                    performance_data["one_month"] = value
                elif label == "3 Month":
                    performance_data["three_months"] = value
                elif label == "YTD":
                    performance_data["year_to_date"] = value
                elif label == "1 Year":
                    performance_data["one_year"] = value
        return performance_data

    def extract_competitors_data(self, soup: BeautifulSoup) -> list:
        table = soup.find("table", class_="table--primary")
        competitors_data = []
        for row in table.find_all("tr", class_="table__row"):
            result_data = {"name": None, "market_cap": None}
            name_cell = row.find("td", class_="table__cell w50")
            if name_cell:
                name = name_cell.get_text(strip=True)
                result_data["name"] = name
                market_cap_cell = row.find("td", class_="table__cell w25 number")
                if market_cap_cell:
                    market_cap_value = market_cap_cell.get_text(strip=True)
                    currency = "USD"
                    if "₩" in market_cap_value:
                        currency = "KRW"
                    elif "¥" in market_cap_value:
                        currency = "JPY"
                    value = re.sub(r"[^\d.]", "", market_cap_value)
                    result_data["market_cap"] = {"currency": currency, "value": value}
                    competitors_data.append(result_data)
        return competitors_data

    def extract_company_name(self, soup: BeautifulSoup) -> str:
        company_name = ""
        company_name_tag = soup.find("h1", class_="company__name")
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
        return company_name
