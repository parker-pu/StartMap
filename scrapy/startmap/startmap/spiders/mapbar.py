import scrapy


class MapBarSpider(scrapy.Spider):
    name = "mapbar"
    allowed_domains = ["mapbar.com"]
    start_urls = ["https://map.mapbar.com/"]

    def parse(self, response):
        """"""
        city_type_dict = {
            "地产": "t_{city_code}_04"
        }
        xpath_str = '//*[@class="latterIndex"]//a[contains(@href,"http://map.mapbar.com")]/@href'
        for city_url in response.xpath(xpath_str).extract():
            city_code = str(city_url).replace("http://map.mapbar.com/", "")
            for model_type, fmt in city_type_dict.items():
                _url = "https://map.mapbar.com/{}".format(fmt.format(city_code=city_code))
                return scrapy.Request(
                    url=_url,
                    callback=self.parse_city_map,
                    dont_filter=False,
                    meta={"model_type": model_type},
                )

    def parse_city_map(self, response):
        """
        解析城市分布
        :param response:
        :return:
        """
        xpath_str = '//*[@class="sty1 margb20"]'
        meta: dict = response.meta
        city_name = str(response.xpath('//h2[@class="educationH2Title"]/text()').extract_first()).strip()
        city_name = city_name.replace("{}分布图".format(meta.get("model_type")), "")
        for _block in response.xpath(xpath_str):
            housing_type = str(_block.xpath('h2[@class="clr"]/text()').extract_first()).strip()
            meta.update({"housing_type": housing_type, "city_name": city_name})
            for housing_url in _block.xpath('p/a/@href').extract():
                yield scrapy.Request(
                    url=str(housing_url).replace("http", "https"),
                    callback=self.parse_housing,
                    dont_filter=False,
                    meta=meta,
                )

    @staticmethod
    def parse_housing(response):
        """
        解析小区数据
        :param response:
        :return:
        """
        meta: dict = response.meta
        print(meta)
        body_xpath = response.xpath('//div[@class="POILeftA"]')
        housing_name = str(body_xpath.xpath('h1[@id="poiName"]/text()').extract_first()).strip()
        if not housing_name or housing_name in ["None"]:
            return
        poi_ula = body_xpath.xpath('div[@class="photoBox"]/div/ul')
        phone = str(poi_ula.xpath('li[@class="telCls"]//text()').extract()[2]).strip()
        housing_item = {
            "housing_name": housing_name,
            "data_update_time": str(poi_ula.xpath('//li/text()').extract_first()).strip().replace("信息更新时间：", ""),
            "addr": "".join(
                [str(x).strip() if "地址" not in x else "" for x in poi_ula.xpath('li[2]//text()').extract()]),
            "phone": None if "无" in phone else phone,
            "housing_type": str(poi_ula.xpath('li[4]//text()').extract()[1]).strip()

        }
        print(housing_item)
