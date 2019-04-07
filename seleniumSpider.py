#【注意：vscode切换python版本，***左下角蓝色条***那里点击切换，做本例时不小心切到anaconda环境造成新装的库不识别了】
from selenium import webdriver
import time

driverNew = webdriver.Chrome()
#打开网址(打开即可，不用再赋值给别的了)
driverNew.get('https://wordpress-edu-3autumn.localprod.forc.work/wp-login.php')
time.sleep(1)
#找到用户表单输入提交
uName = driverNew.find_element_by_id('user_login')
password = driverNew.find_element_by_id('user_pass')
submitButton = driverNew.find_element_by_id('wp-submit')

uName.send_keys('spiderman')#send_keys有s
time.sleep(1)
password.send_keys('crawler334566')
time.sleep(1)

submitButton.submit()
time.sleep(3)
#下拉页面
scrollDown = driverNew.find_element_by_class_name('menu-scroll-down')
#print(scrollDown.text)
scrollDown.click()
#点击第一篇文章
alink = driverNew.find_element_by_id('post-20').find_element_by_tag_name('h2').find_element_by_tag_name('a')
#print(alink.text)
alink.click()
time.sleep(3)
commentBox = driverNew.find_element_by_id('comment')
commentBox.send_keys('阿旺到此一游selenium2019/01/30 第一条')
submitBtn = driverNew.find_element_by_id('submit')
submitBtn.click()
time.sleep(10)
driverNew.close()






