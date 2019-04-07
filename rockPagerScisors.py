#==石头剪刀布：本例为余血PK项目二精华版==
#==函数封装，主函数应用 ，return合理利用，dict巧关联（手动排序可用）==
#.index返回某值在列表中的索引
'''
list = [0,1,0,1,2]
print(list.index(2))#返回2首次出现的索引值
print(list[list.index(2)])
#分别打印4,2
'''
import random,time
#石头剪刀布，电脑和我出拳头比赛

fixList = ['O','X','U']#定义石头剪刀布

myFixList = fixList#定义石头剪刀布
pcFixList =  random.sample(fixList,3)#随机出三个，每次顺序就不一样了
myScore = 0 #计分
pcScore = 0
#选出拳顺序并展示
def chooseFix():
    global myFixList
    myOrderDict = {}
    for i in range(len(myFixList)):
        #order = int(input('你想让 让 '+myFixList[i]+'第几个出场，请打 1 2 3 ')) 
        order = int(input('你想让 让 %s 第几个出场，请打 1 2 3 ' % myFixList[i])) #input里面也可以用%s占位符
        myOrderDict[order] = myFixList[i]
    #print(myOrderDict)
    myFixList = []
    for i in range(1,4):
        myFixList.append(myOrderDict[i])
    time.sleep(1)
    print("===我的出拳头顺序：===")
    for i in range(3):
        print(myFixList[i], end=' ')#不换行打印，拼接下一行
    print("")#打印空行 切断整段与后面end到一起的行
    time.sleep(1)
    print("===电脑的出拳顺序：===")
    for i in range(3):
        print(pcFixList[i], end=' ')
    print("")

    input("输入回车继续")

#三局两胜pk
def pk():
    global myScore
    global pcScore
    global myFixList,pcFixList
    for i in range(3):#三局两胜
        print("\n===【第 %d 局】===\n" % i)
        print("我出：" + myFixList[i])
        print("电脑出：" + pcFixList[i])
        time.sleep(1)
        print("\n==第 %d 局结果：==\n" % i)
        print(judge(myFixList[i],pcFixList[i]))
        time.sleep(1)
    
    input("输入回车看三局两胜成绩")
    print("\n==【看三局两胜成绩】==\n")
    time.sleep(1)
    if myScore > pcScore:
        print("我以 %d : %d 战胜了电脑！～恭喜！～" % (myScore, pcScore))
    elif myScore < pcScore:
        print("电脑以 %d : %d 战胜了我……电脑随机出的有什么可比性是吧，哈哈哈～" % (pcScore, myScore))
    else:
        print("我和电脑 %d : %d 打平了" % (myScore, pcScore))

#判断输赢
def judge(myFix,pcFix):
    global myScore
    global pcScore
    #isWin = (myFix == 'O' and pcFix == 'X') or (myFix == 'X' and pcFix == 'U') or (myFix == 'U' and pcFix == 'O')
    #上面简化如下：【O X U 我出的拳永远比电脑出的拳往前错一位即赢】
    isWin = myFix == fixList[fixList.index(pcFix)-1]#【.index返回某值在列表中的索引，取到往前错一位】
    if myFix == pcFix:
        return "本局平"
    elif isWin:
        myScore = myScore + 1
        return "我赢了！～"
    else:
        pcScore = pcScore +1
        return "我输，电脑赢^^"


#==主函数==
def main():
    chooseFix()
    pk()

main()


