import scrapy

class MySpider(scrapy.Spider):
    name = 'filimo_crawler'

    def start_requests(self):
        urls = [
            'https://www.filimo.com/movies/1/is_dubbed',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        link_list = []
        # استخراج لینک‌ها از تگ <a> با استفاده از xpath
        for i in range(1,100):
            link= response.xpath(f'/html/body/div[1]/main/div/div/section/div/section/div/div/div[{i}]/a/@href').getall()
            link_list.extend(link)
        # ذخیره لینک‌ها به‌صورت فایل متنی
        with open('dataset.txt', 'a+', encoding='utf-8') as f:
            for link in link_list:
                full_link = response.urljoin(link.strip())  # تبدیل لینک به لینک کامل
                f.write(full_link + '\n')