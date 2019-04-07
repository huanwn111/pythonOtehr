import scrapy
#import ..items/DoubanItem格式错误，注意不用/，用from ...import，更正如下：
from ..items import DangdangItem
from bs4 import BeautifulSoup as BS
#==建爬虫类==
class DangdangSpider(scrapy.Spider):#继承中心控制器scrapy引擎的spider类
    #步骤：
    #只需指名爬虫名，网址域，爬取网址。
    #定义解析数据函数pase 使用自己定义的DoubanItem把抓取数据封装到Item并yield返回即可。
    name = 'dangdang'#【爬虫名，运行时的名字 scrapy crawl dangdang】
    allowed_domains  = 'http://bang.dangdang.com'#加域，防址除了抓取网址之外的地址回头再想抓时被忽略
    start_urls  = []
    #【***重要===以上三个变量名不能变，否则框架运行的时候找不到===***】

    for i in range(1,4):
        url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2018-0-1-'+str(i)
        start_urls .append(url)

    def parse(self,res):
        #定义解析提取函数，名字不能变。即可直接使用它的res参数返回抓取结果了。
        #这部分工作相当于下载器做的了
        #print(res.text)
        bsNew = BS(res.text,'html.parser')

        datasList = bsNew.find('ul',class_='bang_list').find_all('li')
        
        for data in datasList:
            #实例化数据封装实体类
            dataItem = DangdangItem()
            #给数据类属性赋值，返回即可，存储工作交给scrapy控制器，分给pipline
            dataItem['num'] = data.find_all('div')[0].text
            dataItem['bookName'] = data.find('div', class_='name').text
            dataItem['author'] = data.find_all('div', class_='publisher_info')[0].text
            dataItem['price'] = data.find('span', class_='price_n').text

            print(dataItem)
            yield dataItem#注意：返回值是可迭代的，用return。返回即可自动传给引擎了。

            #另外注意，dataItem是在for循环里面定义并返回，每一组datas生成一组返回值依次处理。


            








