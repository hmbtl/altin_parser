# -*- coding: utf-8 -*-
import scrapy
import dateparser
from scrapy_selenium import SeleniumRequest


class TapazSpider(scrapy.Spider):
    name = 'tapaz'
    allowed_domains = ['tap.az']
    start_urls = [
        'https://tap.az/elanlar?user_id=14161908',
        'https://tap.az/elanlar?user_id=10514733',
        'https://tap.az/elanlar?user_id=17384093',
        'https://tap.az/elanlar?user_id=15822606',
        'https://tap.az/elanlar?user_id=8165030',
        'https://tap.az/elanlar?user_id=6591188',
        'https://tap.az/elanlar?user_id=13650173'
    ]

    '''
    def start_requests(self):
        for start_url in self.start_urls:
            yield SeleniumRequest(
                url=start_url,
                wait_time=10,
                callback=self.parse,
                dont_filter=True,
                script='window.scrollTo(0, document.body.scrollHeight);',
            )
    '''

    def parse(self, response):
        elans = response.xpath('//div[@class="products-i "]')
        print(len(elans))
        for elan in elans:
            url = elan.xpath(
                ".//a[@class='products-link']/@href").get()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_detail)

        next_page = response.xpath(
            '//div[@class="pagination"]/div[@class="next"]/a/@href').get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page))

    def parse_detail(self, response):
        info = {}
        title = response.xpath(
            "//div[@class='title-container']/h1/text()").get()
        price = response.xpath(
            "//div[@class='price-container']//span[@class='price-val']/text()").get()
        phone = response.xpath("//a[@class='phone']/text()").get()
        desc_extracted = response.xpath(
            "//div[@class='lot-text']/p/text()").extract()
        desc = u' '.join(desc_extracted)
        image = response.xpath("//a[@class='large-photo']/@href").get()
        otherPictures = response.xpath(
            "//div[@class='thumbnails']/a/@href").getall()

        # yield values
        info = {
            'title': title,
            'url': response.url,
            'price': price,
            'desc': desc,
            'image': image,
            "phone": phone,
            "otherPictures": otherPictures
            # "features": features
        }

        for feature in response.xpath('//tr[@class="property"]'):
            label = feature.xpath(
                './/td[@class="property-name"]/text()').get()
            value = feature.xpath(
                './/td[@class="property-value"]/text()').get()
            info[label] = value

        # yield values
        yield info
