import time
import requests
import pymysql
from lxml import etree



class BaseSpider(object):
    def __init__(self, base_url):
        self.url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            # 'Cookie': 'Hm_lvt_35d5cf95646cd40f596aba2746c97bde=1587380041,1587449215,1587529988,1589173871; jieqiVisitId=article_articleviews%3D152384%7C148324%7C147834%7C151770; Hm_lpvt_35d5cf95646cd40f596aba2746c97bde=1589206262',
            'Connection': 'close'
        }

    # 获取小说url
    def get_category_book(self):
        response = requests.get(self.url, headers=self.headers, verify=False).content.decode('gbk')
        # response = requests.get(self.url).content.decode('gbk')
        html = etree.HTML(response)

        book_urls = html.xpath('//div[contains(@class, "news")]/ul/li/span[2]/a/@href')

        return book_urls

    # 获取小说信息
    def get_book_info(self, url):
        response = requests.get(url, headers=self.headers, verify=False)
        # response = requests.get(url)
        # 获取网页url, 用于拼接章节url
        base_url = response.url

        content = response.content.decode('gbk')
        html = etree.HTML(content)

        # 获取小说信息
        book_infos = html.xpath('//div[@class="book_info"]')
        for book_info in book_infos:
            book_name = book_info.xpath('./div[@id="info"]/h1/text()')[0]
            author_name = book_info.xpath('./div[@id="info"]//span[1]/a/text()')[0]
            cover = book_info.xpath('./div[@class="pic"]/img/@src')[0]
            intro = book_info.xpath('./div[@id="info"]/div[@class="bookinfo_intro"]/text()')
            intro = ''.join(intro).replace(' ', '')
            book_chapters_urls = html.xpath('//div[@class="book_list"]/ul/li/a/@href')
            book_chapters = []
            for book_chapters_url in book_chapters_urls:
                book_chapters_url = base_url + book_chapters_url
                book_chapters.append(book_chapters_url)

            item = {
                'book_name': book_name,
                'author_name': author_name,
                'cover': cover,
                'intro': intro,
                'book_chapters_url': book_chapters
            }

            return item

    # 获取章节内容
    def get_chapter_content(self, url):
        # 获取章节内容
        response = requests.get(url, headers=self.headers, verify=False)
        # response = requests.get(url)
        try:
            content = response.content.decode('gbk')
        except:
            content = response.content.decode()

        html = etree.HTML(content)
        chapter_name = html.xpath('//div[@class="h1title"]/h1/text()')[0]
        content = html.xpath('//div[@id="htmlContent"]/text()')[1:]
        content = ''.join(content)
        word_count = len(content)

        return chapter_name, content, word_count

    def stored_mysql(self, items, cate_id, channel_id):
        conn = pymysql.connect(
            host="192.168.38.20",
            user="root",
            password="mysql",
            database="ibook_db",
            charset="utf8")

        # 创建游标对象
        cursor = conn.cursor()

        for item in items:
            print(item)
            # 插入图书
            inset_sql = """
                insert into book(`id`, `book_name`, `author_name`, `is_publish`, `status`, `cover`, `intro`, `showed`, `collect_count`, `heat`, `cate_id_id`,`channel_type_id`) values(null, %s, %s, 1, 1, %s, %s, 1, 0, 0, %s, %s)
            """
            cursor.execute(inset_sql,
                           (item['book_name'], item['author_name'], item['cover'], item['intro'], cate_id, channel_id))
            conn.commit()

            # 获取图书id
            select_book_id = """
                select id from book where book_name = "%s"
            """ % item['book_name']

            cursor.execute(select_book_id)
            book_id = cursor.fetchone()

            # 插入章节信息
            for chapter_info in item['chapter_info']:
                insert_capter_sql = """
                    insert into book_chapters(`id`, `chapter_name`, `word_count`, `book_id_id`) values(null, %s, %s, %s)
                """
                cursor.execute(insert_capter_sql, (chapter_info['chapter_name'], chapter_info['word_count'], book_id))
                conn.commit()

                # 查找图书章节id
                select_capter_id = """
                    select id from book_chapters where chapter_name= "%s" and book_id_id="%s"
                """ % (chapter_info['chapter_name'][0], book_id[0])
                cursor.execute(select_capter_id)
                chapter_id = cursor.fetchone()

                # 插入图书章节内容
                insert_book_content = """
                    insert into book_chapter_content(`id`, `content`, `book_id_id`, `chapter_id_id`) values(null, %s, %s, %s)
                """
                cursor.execute(insert_book_content, (chapter_info['content'], book_id, chapter_id))
                conn.commit()

    def run(self, cate_id, channel_id):
        print('爬虫开始')
        book_urls = self.get_category_book()
        items = []
        for book_url in book_urls[0:15]:
            print('爬取小说信息开始')
            item = self.get_book_info(book_url)
            print('爬取小说信息完成')
            chapter_infos = []
            for url in item['book_chapters_url']:
                time.sleep(1)
                chapter_info = {}
                chapter_name, content, word_count = self.get_chapter_content(url)
                print('爬取小说小说章节内容--', chapter_name)
                chapter_info['chapter_name'] = chapter_name,
                chapter_info['content'] = content,
                chapter_info['word_count'] = word_count

                chapter_infos.append(chapter_info)
                print('爬取小说小说章节内容完成')

                item['chapter_info'] = chapter_infos
            items.append(item)
        print(items)
        print('小说开始入库')
        self.stored_mysql(items, cate_id=cate_id, channel_id=channel_id)
        print('小说入库完成')


if __name__ == '__main__':
    BaseSpider(base_url='https://www.50zw.com/1_1/').run(cate_id=1, channel_id=1)
