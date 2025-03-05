import datetime
import json
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict, Optional
from phi.tools import Toolkit
from phi.utils.log import logger
from dotenv import load_dotenv
load_dotenv()


# --- Supported Coupon Websites ---
COUPON_SITES = {
    "retailmenot": "https://www.retailmenot.com/view/{store}",
    "coupons": "https://www.coupons.com/coupon-codes/{store}",
    "honey": "https://www.joinhoney.com/shop/{store}",
    # "groupon": "https://www.groupon.com/coupons/stores/{store}",
    # "slickdeals": "https://slickdeals.net/coupons/{store}/",
    # "dealspotr": "https://dealspotr.com/promo-codes/{store}"
}

# --- Proxy List for Scraping ---
PROXY_LIST = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    "http://proxy3.com:8080"
]


class PromoCodeScraper(Toolkit):
    """Tool for scraping promo codes from coupon websites with rotating headers & proxies."""

    def __init__(self):
        super().__init__(name="promo_code_scraper")
        self.register(self.scrape_promo_codes)

    def scrape_promo_codes(self, store: str, source: str = "retailmenot") -> List[Dict]:
        """Scrapes promo codes from a given coupon website."""
        if source not in COUPON_SITES:
            return [{"error": f"Unsupported source. Choose from: {', '.join(COUPON_SITES.keys())}"}]

        url = COUPON_SITES[source].format(store=store)
        headers = {"User-Agent": UserAgent().random}
        proxy = {"http": random.choice(PROXY_LIST)}

        logger.info(f"Fetching promo codes from: {url}")

        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch data: {e}")
            return [{"error": f"Failed to fetch data: {str(e)}"}]

        soup = BeautifulSoup(response.text, "html.parser")
        promo_codes = []

        try:
            if source == "retailmenot":
                for code_section in soup.find_all("div", class_="coupon-code"):
                    code = code_section.get_text(strip=True)
                    discount = code_section.find_next_sibling("span", class_="discount-value")
                    expiry = code_section.find_next_sibling("span", class_="expiration-date")

                    promo_codes.append({
                        "promo_code": code,
                        "discount": discount.get_text(strip=True) if discount else "Unknown",
                        "expires": expiry.get_text(strip=True) if expiry else "No Expiry"
                    })
            elif source == "coupons":
                for deal in soup.find_all("div", class_="deal-tile"):
                    code = deal.find("span", class_="code").get_text(strip=True) if deal.find("span", class_="code") else "No Code"
                    discount = deal.find("span", class_="discount").get_text(strip=True) if deal.find("span", class_="discount") else "Unknown"
                    expiry = deal.find("span", class_="expiry").get_text(strip=True) if deal.find("span", class_="expiry") else "No Expiry"

                    promo_codes.append({
                        "promo_code": code,
                        "discount": discount,
                        "expires": expiry
                    })
            
            logger.info(f"Scraped {len(promo_codes)} promo codes.")
            return promo_codes if promo_codes else [{"message": "No promo codes found."}]
        except Exception as e:
            logger.warning(f"Error parsing promo codes: {e}")
            return [{"error": f"Parsing failed: {str(e)}"}]


class CurrentDateTimeTool(Toolkit):
    """Tool to fetch the current date and time."""

    def __init__(self):
        super().__init__(name="current_datetime_tool")
        self.register(self.get_current_datetime)
    
    def get_current_datetime(self) -> str:
        """Returns the current date and time in a human-readable format."""
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y %H:%M:%S')}."


class ShippingTimeEstimator(Toolkit):
    """
    Tool to estimate shipping feasibility, cost, and delivery date.
    """

    def __init__(self):
        super().__init__(name="shipping_time_estimator")
        self.register(self.estimate_shipping)

    def estimate_shipping(self, location: str, delivery_date: str, weight: Optional[float] = None) -> List[Dict]:
        """Estimates shipping feasibility, cost, and delivery date."""
        today = datetime.date.today()
        
        try:
            desired_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d").date()
        except ValueError:
            logger.warning("Invalid date format. Expected YYYY-MM-DD.")
            return [{"error": "Invalid date format. Please use YYYY-MM-DD."}]

        estimated_days = 3
        base_cost = 10.0
        weight_cost = (weight * 0.5) if weight else 0
        estimated_cost = base_cost + weight_cost

        feasibility = "Feasible" if desired_date >= today + datetime.timedelta(days=estimated_days) else "Not Feasible"
        estimated_arrival = today + datetime.timedelta(days=estimated_days)

        logger.info(f"Shipping estimation for {location}: Cost = ${estimated_cost:.2f}, Feasibility = {feasibility}")

        return [{
            "feasibility": feasibility,
            "estimated_cost": f"${estimated_cost:.2f}",
            "estimated_arrival_date": estimated_arrival.strftime("%Y-%m-%d"),
        }]


class UserLocationTool(Toolkit):
    """Tool to fetch the user's current location based on IP address."""

    def __init__(self):
        super().__init__(name="user_location_tool")
        self.register(self.get_user_location)

    def get_user_location(self) -> List[Dict]:
        """Fetches the user's location based on IP address."""
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            response.raise_for_status()
            data = response.json()

            location_info = {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "latitude_longitude": data.get("loc", "Unknown"),
                "timezone": data.get("timezone", "Unknown")
            }

            logger.info(f"User location fetched: {location_info}")
            return [location_info]
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch location: {e}")
            return [{"error": "Failed to retrieve location."}]
