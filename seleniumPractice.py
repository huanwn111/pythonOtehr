#==取python之禅英文版 selenium find elemtnt .text , driver.page_source==
#方法一：用selenium的find element后 .text取文字(其它还有.get_attribute)
#方法二：用driver.page_source取得页面编码转BS对象取值

from selenium import webdriver
import time
from bs4 import BeautifulSoup as BS

driver = webdriver.Chrome()

driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/')
time.sleep(2)#这里要睡眠2s等下面页面元素加载后才能取到

input1 = driver.find_element_by_id('teacher')
#输入文字
input1.send_keys('吴枫')
time.sleep(1)

input2 = driver.find_element_by_id('assistant')
input2.send_keys('保密')
time.sleep(1)

submitBtn = driver.find_element_by_class_name('sub')
#提交
submitBtn.click()#单击即可，不用submit
time.sleep(1)

#到另一页面了，取python之禅英文版
#方法一：用selenium的find element后 .text取文字(其它还有.get_attribute)
'''
enPythonWords = driver.find_elements_by_class_name('content')[0]
rs = enPythonWords.text
'''
#方法二：用driver.page_source取得页面编码转BS对象取值
rsHtml = driver.page_source
rsHtmlObj = BS(rsHtml,'html.parser')
rs = rsHtmlObj.find_all('div', class_='content')[0].text
print(rs)

driver.close()#别忘了关闭

