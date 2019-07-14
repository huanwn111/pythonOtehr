import pyautogui
import time

def saveImg():
    dur = 0.5
    pyautogui.PAUSE = 0.05#脚本执行完暂停1.5s 控制鼠标
    pyautogui.FAILSAFE = True#想终止程序可快速将鼠标移到屏幕左上角

    #移动鼠标

    #获取屏幕分辨率
    #width,height = pyautogui.size()

    #print((width,height))#(1366, 768)


    
    #移到文件点击
    time.sleep(0.8)

    x1 = 284
    y1= 64

    pyautogui.moveTo(x1,y1,duration=dur)#移动
    pyautogui.click(x=x1, y=y1, button='left')#点击,默认点当前位置
    time.sleep(0.5)
    #pyautogui.click(button='left')
    pyautogui.click(x=x1, y=y1, button='left')
    

    #移到另存为点击
    x2 = 284
    y2= 240

    pyautogui.moveTo(x2,y2,duration=dur)#移动
    pyautogui.click(x=x2, y=y2, button='left')

    #移到保存类型，先png保存
    x3= 550
    y3= 690

    x4= 550
    y4= 670

    x5= 960
    y5= 730

    x6= 760
    y6= 390

    pyautogui.moveTo(x3,y3,duration=dur)#移动
    pyautogui.click(x=x3, y=y3, button='left')#点击
    pyautogui.moveTo(x4,y4,duration=dur)#移动
    pyautogui.click(x=x4, y=y4, button='left')#点击
    #保存
    pyautogui.moveTo(x5,y5,duration=dur)#移动
    pyautogui.click(x=x5, y=y5, button='left')#点击
    #确认保存
    pyautogui.moveTo(x6,y6,duration=dur)#移动
    pyautogui.click(x=x6, y=y6, button='left')#点击

    #关闭
    x7 = 1160
    y7 = 35
    pyautogui.moveTo(x7,y7,duration=dur)#移动
    pyautogui.click(x=x7, y=y7, button='left')#点击
    time.sleep(0.5)

    #确认关闭
    x8 = 750
    y8 = 420
    pyautogui.moveTo(x8,y8,duration=dur)#移动
    pyautogui.click(x=x8, y=y8, button='left')#点击
    time.sleep(0.5)

    #离开画图工具（循环执行时点击文件不一致，需离开画图工具再激活）
    x9 = 1290
    y9 = 300
    pyautogui.moveTo(x9,y9,duration=dur)#移动
    pyautogui.click(x=x9, y=y9, button='left')#点击



for i in range(20):
    
    saveImg()
    time.sleep(1)


#saveImg()
