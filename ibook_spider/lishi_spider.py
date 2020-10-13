from ibook_spider.base_spider import BaseSpider

url = 'https://www.50zw.com/4_1/'
BaseSpider(base_url=url).run(cate_id=4, channel_id=1)
