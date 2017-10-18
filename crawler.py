import sys
import scrapy

if len(sys.argv) < 2:
    print('This crawler takes exactly two arguments [URL] [email]')
    exit(-1)


class LBCSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(LBCSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]

    name = 'lbc'

    def parse(self, response):
        number_of_results = response.xpath('//*[@id="listingAds"]/section/header/nav/a/span/text()').extract()[
            0].replace(' ', "")
        number_of_results = int(number_of_results)
        yield {
            "count": number_of_results
        }

        for r in response.xpath('//*[@id="listingAds"]/section/section/ul/li/a'):
            try:
                o = Object()
                o.title = r.xpath(".//section/h2/text()").extract_first().strip()
                o.location = r.xpath(".//section/p[2]/meta[1]/@content").extract_first() + ' / ' \
                         + r.xpath(".//section/p[2]/meta[2]/@content").extract_first()
                o.price = self.parse_price(r.xpath(".//section/h3/text()").extract_first().strip())
                o.date_pub = r.xpath(".//section/aside/p/text()").extract_first().strip()
                o.href = r.xpath('.//@href').extract_first()
                yield o.serialize()

            except (TypeError, AttributeError):
                pass


    def parse_price(self, price):
        return price.replace(u'\u00a0', '').replace(u'\u20ac', '')


class Object:
    title = ""
    location = ""
    price = ""
    date_pub = ""
    href = ""

    def serialize(self):
        return {
            "title": self.title,
            "location": self.location,
            "price": self.price,
            "date_pub": self.date_pub,
            'href': self.href
        }
