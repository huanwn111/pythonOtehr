from wxpy import *
import time
#pip3 install -U wxpy 或如下安装
#pip3 install -U wxpy -i "https://pypi.doubanio.com/simple/"
bot = Bot()

#给好友发消息
#my_friend = bot.friends().search('游戏代练')[0];

#my_friend.send('早准备睡的早，准备睡觉吧');
#给自己发消息
#bot.file_helper.send('准备睡觉吧，早准备睡的早');

#发群消息
#my_group = bot.groups().search('Python小课-山顶群(4)')[0];
#my_group.send("再冒险试下发群消息，如果明天我不见了，就是被封了");
'''
my_group2 = bot.groups().search('和谐好伙伴')[0];
my_group2.send_image('D:\img\100.jpg');
my_group2.send('你好，我是小器');
'''
#给好友群发消息

my_friends = ['阿旺','游戏代练','延君','spirit'];
for item in my_friends:
    friendItem = bot.friends().search(item)[0];
    info = item+'，早上好，我是旺旺旺派来的，哈哈哈~~~'
    print(info)
    friendItem.send(info)
    time.sleep(3)



#微信机器人发消息
#参考https://wxpy.readthedocs.io/zh/latest/
#https://blog.csdn.net/sm9sun/article/details/79725637
#https://blog.csdn.net/sm9sun/article/details/79725637