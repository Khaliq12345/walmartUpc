from selectolax.parser import HTMLParser
from the_retry import retry
import json
from typing import Optional
import hrequests

TIMEOUT = 50000
SWITCHER_SELECTOR = 'a[class="lang-switcher"]'
completed = []
items = []

ca_proxy_dict = {
    "server": "us.decodo.com:10000",
    "username": "eezlyuser",
    "password": "E87lb_nGg1gaIcmuB4",
}

test_url = "https://www.walmart.ca/fr/ip/6000203653001"


def get_upc_from_json_data(json_data: dict) -> Optional[str | None]:
    upc = None
    try:
        for x in json_data["props"]["pageProps"]["initialData"]["data"]["idml"][
            "specifications"
        ]:
            if ("UPC" in x["name"]) or ("CUP" in x["name"]):
                upc = x["value"]
                break
    except Exception as e:
        print(f"UPC Error: {e}")
        upc = None

    return upc


@retry(attempts=5, backoff=2)
def scraper_v2(url: str) -> str:
    proxy = {
        "http": f"http://{ca_proxy_dict['username']}:{ca_proxy_dict['password']}@{ca_proxy_dict['server']}",
        "https": f"https://{ca_proxy_dict['username']}:{ca_proxy_dict['password']}@{ca_proxy_dict['server']}",
    }
    response = hrequests.get(url, proxy=proxy["https"])
    soup = HTMLParser(response.text)
    json_str = soup.css_first('script[id="__NEXT_DATA__"]').text()
    json_data = json.loads(json_str)
    return get_upc_from_json_data(json_data)


if __name__ == "__main__":
    print(scraper_v2(test_url))
