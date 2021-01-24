# -*- coding: utf-8 -*-
import scrapy
import dateparser


class UnimallSpider(scrapy.Spider):
    name = 'unimall'
    allowed_domains = ['unimall.az']
    start_urls = ['https://unimall.az/jewellery-999/', 'https://unimall.az/ro-gold/',
                  'https://unimall.az/baku-gold/', 'https://unimall.az/celilov-gold/']

    def parse(self, response):
        for jobs in response.xpath('//div[@class="ty-column4"]'):
            url = jobs.xpath(
                ".//div[@class='ty-grid-list__item   th_grid-list__item ty-quick-view-button__wrapper']/meta[@itemprop='url']/@content").get()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_detail)
        next_page = response.xpath(
            '//a[@class="ty-pagination__item ty-pagination__btn ty-pagination__next cm-history cm-ajax cm-ajax-full-render"]/@href').get()

        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page))

    def decode_email(self, e):
        de = ""
        k = int(e[:2], 16)
        for i in range(2, len(e)-1, 2):
            de += chr(int(e[i:i+2], 16) ^ k)
        return de

    def parse_detail(self, response):
        # get start date and parse to correct string
        #start_date_str = response.xpath('//div[@class="bumped_on params-i-val"]/text()').get()
        #start_date = dateparser.parse(start_date_str).strftime('%d/%m/%Y')
        info = {}

        title = response.xpath(
            '//h1[@class="ty-product-block-title"]/text()').get()
        price = response.xpath('//span[@class="ty-price-num"]/text()').get()
        desc_extracted = response.xpath(
            '//div[@id="content_description"]/div[2]/text()').extract()
        desc = u' '.join(desc_extracted)
        image = response.xpath(
            '//a[@class="cm-image-previewer cm-previewer ty-previewer"]/@href').get()
        phone = response.xpath(
            '//a[@class="compnumber ty-link_clickable"]/text()').get()

        # yield values
        info = {
            'title': title,
            'url': response.url,
            'price': price,
            'desc': desc,
            'image': "http://unimall.az/" + image,
            "phone": phone,
            # "features": features
        }

        #features = {}
        for feature in response.xpath('//div[@class="ty-product-feature"]'):
            label = feature.xpath(
                './/span[@class="ty-product-feature__label"]/text()').get()
            label = label[:-1]
            value = feature.xpath(
                './/li[@class="ty-product-feature__multiple-item"]/text()').get()
            info[label] = value

        yield info
