import logging
import re

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from server.core.settings import Settings, settings

logger = logging.getLogger(__name__)


class MarketWatchScraper:
    def __init__(self, skip_browser: bool = False, context: Settings = settings):
        self.data = {}
        self._context = context
        self._link = self._context.MARKETWATCH_URI
        self._headless = skip_browser
        self._user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )

    def run(self, company: str) -> dict:
        url = "{}/{}".format(self._link, company)
        html = self.fetch_data(url)
        soup = BeautifulSoup(html, "html.parser")
        self.data["company_code"] = company.upper()
        self.data["company_name"] = self.extract_company_name(soup)
        self.data["performance"] = self.extract_performance_data(soup)
        self.data["competitors"] = self.extract_competitors_data(soup)
        return self.data

    def fetch_data(self, url: str) -> str:
        player = sync_playwright().start()
        browser = player.chromium.launch(headless=self._headless)
        context = browser.new_context(user_agent=self._user_agent)
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(15000)
        # page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state("networkidle")
        page_content = page.content()
        browser.close()
        return page_content

    def extract_performance_data(self, soup:BeautifulSoup)-> dict:
        table = soup.find('table', class_='table--primary')
        performance_data = {}
        for row in table.find_all('tr', class_='table__row'):
            cells = row.find_all('td', class_='table__cell')
            if len(cells) == 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].find('li', class_='content__item value').get_text(strip=True)
                if label == '5 Day':
                    performance_data['five_days'] = value
                elif label == '1 Month':
                    performance_data['one_month'] = value
                elif label == '3 Month':
                    performance_data['three_months'] = value
                elif label == 'YTD':
                    performance_data['year_to_date'] = value
                elif label == '1 Year':
                    performance_data['one_year'] = value
        return performance_data

    def extract_competitors_data(self, soup:BeautifulSoup)-> list:
        table = soup.find('table', class_='table--primary')
        competitors_data = []
        for row in table.find_all('tr', class_='table__row'):
            result_data = {"name": None, "market_cap": None}
            name_cell = row.find('td', class_='table__cell w50')
            if name_cell:
                name = name_cell.get_text(strip=True)
                result_data["name"] = name
                market_cap_cell = row.find('td', class_='table__cell w25 number')
                if market_cap_cell:
                    market_cap_value = market_cap_cell.get_text(strip=True)
                    currency = 'USD'
                    if '₩' in market_cap_value:
                        currency = 'KRW'
                    elif '¥' in market_cap_value:
                        currency = 'JPY'
                    value = re.sub(r'[^\d.]', '', market_cap_value)
                    result_data["market_cap"] = {'currency': currency,'value': value}
                    competitors_data.append(result_data)
        return competitors_data

    def extract_company_name(self, soup: BeautifulSoup) -> str:
        company_name = ""
        company_name_tag = soup.find("h1", class_="company__name")
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
        return company_name
