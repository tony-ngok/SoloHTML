import json


class HTMLPipeline:
    URL_FORMAT = "https://www.tiktok.com/view/product/"
    # 例：https://www.tiktok.com/view/product/1729527313880355335

    pathes = []

    def __init__(self, pathes: list) -> None:
        self.pathes = pathes

    def test_product_pipeline(self):
        """
        流程：提取商品号，进入并下载商品明细网页
        """

        for path in self.pathes:
            with open(path, "r", encoding="utf-8") as file:
                for data in file.readlines():
                    product = json.loads(data)
                    url = self.URL_FORMAT+product["id"]


if __name__ == '__main__':
    pathes = [
        "tiktok_test/pages/tk_product_seeds.txt",
        "tiktok_test/pages/tk_product_seeds-1.txt",
        ]
    
    HTMLPipeline(pathes).test_product_pipeline()
