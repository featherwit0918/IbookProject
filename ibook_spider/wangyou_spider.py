from ibook_spider.base_spider import BaseSpider

url = 'https://www.50zw.com/5_1/'
BaseSpider(base_url=url).run(cate_id=5, channel_id=1)
