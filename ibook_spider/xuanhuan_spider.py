from ibook_spider.base_spider import BaseSpider

url = 'https://www.50zw.com/1_1/'
BaseSpider(base_url=url).run(cate_id=1, channel_id=1)
