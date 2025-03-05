from langchain.tools import StructuredTool
import datetime
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging
import requests
from langchain_community.document_loaders.firecrawl import FireCrawlLoader

logger = logging.getLogger(__name__)

#  Promo Code Scraper
COUPON_SITES = {
    "retailmenot": "https://www.retailmenot.com/view/{store}",
    "coupons": "https://www.coupons.com/coupon-codes/{store}",
    "honey": "https://www.joinhoney.com/shop/{store}",
}

def scrape_promo_codes(store: str, source: str = "retailmenot") -> List[Dict]:
    """
    Scrapes promo codes from coupon websites like RetailMeNot, Coupons.com, and Honey.

    Args:
        store (str): The store name (e.g., "amazon").
        source (str): The coupon website (default: "retailmenot").

    Returns:
        List[Dict]: A list of promo codes with discounts and expiration dates.
    """
    if source not in COUPON_SITES:
        return [{"error": f"Unsupported source. Choose from: {', '.join(COUPON_SITES.keys())}"}]

    url = COUPON_SITES[source].format(store=store)
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
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

    except Exception as e:
        return [{"error": f"Parsing failed: {str(e)}"}]

    return promo_codes if promo_codes else [{"message": "No promo codes found."}]

PromoCodeScraper = StructuredTool.from_function(
    scrape_promo_codes,
    name="promo_code_scraper",
    description="Scrapes promo codes from coupon websites."
)


# 🔹 Current Date and Time
def get_current_datetime() -> str:
    """
    Returns the current date and time in a human-readable format.
    """
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y %H:%M:%S')}."

CurrentDateTimeTool = StructuredTool.from_function(
    get_current_datetime,
    name="current_datetime_tool",
    description="Returns the current date and time."
)


#  Shipping Time Estimator
def estimate_shipping(location: str, delivery_date: str, weight: Optional[float] = None) -> Dict:
    """
    Estimates shipping feasibility, cost, and delivery date.

    :param location: Destination of the shipment.
    :param delivery_date: User's desired delivery date (YYYY-MM-DD).
    :param weight: (Optional) Weight of the package in kg.
    :return: Dictionary containing feasibility, cost, and estimated delivery date.
    """
    today = datetime.date.today()
    
    try:
        desired_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    estimated_days = 3
    base_cost = 10.0
    weight_cost = (weight * 0.5) if weight else 0
    estimated_cost = base_cost + weight_cost

    feasibility = "Feasible" if desired_date >= today + datetime.timedelta(days=estimated_days) else "Not Feasible"
    estimated_arrival = today + datetime.timedelta(days=estimated_days)

    return {
        "feasibility": feasibility,
        "estimated_cost": f"${estimated_cost:.2f}",
        "estimated_arrival_date": estimated_arrival.strftime("%Y-%m-%d"),
    }

ShippingTimeEstimator = StructuredTool.from_function(
    estimate_shipping,
    name="shipping_time_estimator",
    description="Estimates shipping cost and delivery time."
)




def get_current_location() -> Dict:
    """
    Retrieves the user's current location using IP-based geolocation.

    Returns:
        Dict: A dictionary containing city, region, country, and latitude/longitude.
    """
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()

        location_data = {
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "country": data.get("country", "Unknown"),
            "latitude": data.get("loc", "Unknown").split(",")[0] if data.get("loc") else "Unknown",
            "longitude": data.get("loc", "Unknown").split(",")[1] if data.get("loc") else "Unknown",
            "ip": data.get("ip", "Unknown")
        }
        return location_data

    except requests.RequestException as e:
        return {"error": f"Failed to retrieve location: {str(e)}"}

CurrentLocationTool = StructuredTool.from_function(
    get_current_location,
    name="current_location",
    description="Retrieves the user's approximate current location using IP geolocation."
)

def calculator(operation: str, num1: float, num2: float) -> Dict:
    """
    Performs basic arithmetic operations.

    Args:
        operation (str): The mathematical operation ('add', 'subtract', 'multiply', 'divide').
        num1 (float): First number.
        num2 (float): Second number.

    Returns:
        Dict: The result of the operation.
    """
    if operation not in {"add", "subtract", "multiply", "divide"}:
        return {"error": "Invalid operation. Use 'add', 'subtract', 'multiply', or 'divide'."}
    
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return {"error": "Division by zero is not allowed."}
        result = num1 / num2

    return {"operation": operation, "num1": num1, "num2": num2, "result": result}

CalculatorTool = StructuredTool.from_function(
    calculator,
    name="calculator",
    description="Performs basic arithmetic operations (add, subtract, multiply, divide)."
)




def scrape_and_crawl(url: str) -> List[Dict]:
    """
    Uses Firecrawl to scrape and crawl a given URL.

    Args:
        url (str): The webpage URL to scrape.

    Returns:
        List[Dict]: Extracted text and metadata from the page.
    """
    try:
        loader = FireCrawlLoader(urls=[url])
        docs = loader.load()
        
        results = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "title": doc.metadata.get("title", "Untitled"),
                "content": doc.page_content[:1000]  # Limiting to first 1000 chars
            }
            for doc in docs
        ]

        return results if results else [{"message": "No data extracted."}]
    
    except Exception as e:
        return [{"error": f"Failed to scrape: {str(e)}"}]

ScrapeAndCrawlTool = StructuredTool.from_function(
    scrape_and_crawl,
    name="scrape_and_crawl",
    description="Scrapes and crawls a given webpage URL to extract text and metadata."
)