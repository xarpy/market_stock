import logging

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

    def run(self, company: str):
        url = "{}/{}".format(self._link, company)
        html = self.fetch_data(url)
        soup = BeautifulSoup(html, "html.parser")
        self.data["company_code"] = company.upper()
        self.data["company_name"] = self.extract_company_name(soup)
        self.data["performance"] = self.extract_performance_data(soup)
        self.data["competitors"] = self.extract_competitors_data(soup)
        return self.data

    def fetch_data(self, url: str):
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

    def extract_performance_data(self, soup):
        result = {}
        performance_section = soup.find("section", class_="performance")
        if performance_section:
            performance_data = [item.get_text(strip=True) for item in performance_section.find_all("span")]
            if performance_data:
                result.update(
                    {
                        "five_days": performance_data[0],
                        "one_month": performance_data[1],
                        "three_months": performance_data[2],
                        "year_to_date": performance_data[3],
                        "one_year": performance_data[4],
                    }
                )
        return result

    def extract_competitors_data(self, soup):
        result = []
        competitors_section = soup.find("section", class_="Competitors")
        if competitors_section:
            competitors = [comp.get_text(strip=True) for comp in competitors_section.find_all("li")]
            result = [{"name": comp} for comp in competitors]
        return result

    def extract_company_name(self, soup):
        company_name = ""
        company_name_tag = soup.find("h1", class_="company__name")
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
        return company_name
