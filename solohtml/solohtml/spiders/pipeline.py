import json
from os.path import abspath, dirname, join

import scrapy
from scrapy.http import HtmlResponse


# scrapy crawl solo_html
class SoloHTMLSpider(scrapy.Spider):
    name = "solo_html"
    allowed_domains = ['www.tiktok.com']
    URL_FORMAT = "https://www.tiktok.com/view/product/"
    # 例：https://www.tiktok.com/view/product/1729527313880355335

    pathes = [
        # 这两个txt中一共5240条记录
        "tiktok_test/datasource/tk_product_seeds.txt",
        "tiktok_test/datasource/tk_product_seeds-1.txt"
    ]

    prod_id = ""
    prod_ids = set()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prod_id = ""
        self.prod_ids = set()

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh;q=0.6",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            # "cookie": "your_cookie_here",
            "Referer": "https://www.tiktok.com",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"
        }

    def start_requests(self):
        for path in self.pathes:
            with open(path, "r", encoding="utf-8") as file:
                for data in file.readlines():
                    product = json.loads(data)
                    url = self.URL_FORMAT+product["id"]
                    self.prod_id = product["id"]

                    if self.prod_id not in self.prod_ids:
                        self.prod_ids.add(self.prod_id)
                        yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response: HtmlResponse):
        path = join(dirname(abspath(__file__)), 'tiktok_test/htmls', f"p{self.prod_id}.html")
        with open(path, "wb") as f:
            f.write(response.body)
