#==余血PK小游戏升级版 在blood2函数封装的基础上改成 类封装，并增加角色相互克制，抱团互补等功能，按需修改类方法类属性==

import random, time
#增加角色信息类
class Role:
    
    def __init__(self, name = '【普通角色】'):
        self.name = name
        self.blood = random.randint(100,150)
        self.fight = random.randint(30,50)

    #def showInfo(self):
    #    print("%s 的血量 %d ：攻击力 %d :" % (self.name,self.blood,self.fight))

class Knight(Role):

    def __init__(self, name = '【圣光骑士】'):
        Role.__init__(self, name)#name没改写，只传了不同的参数，继承父类的
        #self.blood = 5*random.randint(100,150)#血量，攻击力都改写了
        #self.fight = 3*random.randint(30,50)
        #【此处算算错误，不是再生成随机数，是现在blood改变，以下同】
        self.blood = int(self.blood*1.5)
        self.fight = int(self.fight*0.8)
    
    #增加互克类，【圣光骑士】遇【暗影刺客】攻击力增加50%
    def fightBuff(self, opponent, str1, str2):
        if opponent.name == '【暗影刺客】':
            self.fight = int(1.5*self.fight)
            print('『%s』【圣光骑士】对 『%s』【暗影刺客】说：“让无尽光芒制裁你的堕落！”'%(str1, str2))
    #【解析：重点，总结==：
        #opponent此处可理解为：旨在练习类方法接收外部参数，跟据参数互动，来修改方法，
        # 参数可以是其它的东西，
        # 只不过此例是三个角色互克，所以这里要传入一个一模一样的角色对象哦，取它的name判断】
    #使用：在Blood3Class类的pk方法中使用，
    # self.myRoles[i].fightBuff(self.enemyRoles[i])，
    # 当敌方的i与我方的i刚好匹配到克制关系时即攻击力按规则变化

class Assassin(Role):

    def __init__(self, name = '【暗影刺客】'):
        Role.__init__(self,name)#name继承父类
        #self.blood = 3*random.randint(100,150)
        #self.fight = 5*random.randint(30,50)
        self.blood = int(self.blood*0.8)
        self.fight = int(self.fight*1.5)

    #增加互克类，【暗影刺客】遇【精灵弩手】攻击力增加50%
    def fightBuff(self, opponent, str1, str2):
        if opponent.name == '【精灵弩手】':
            self.fight = int(1.5*self.fight)
            print('『%s』【暗影刺客】对 『%s』【精灵弩手】说：“主动找死，就别怪我心狠手辣。”'%(str1, str2))
class Bowman(Role):
    
    def __init__(self, name = '【精灵弩手】'):
        Role.__init__(self,name)#name继承父类
        #self.blood = 4*random.randint(100,150)
        #self.fight = 4*random.randint(30,50)
        self.blood = int(self.blood*1.2)
        self.fight = int(self.fight*1.2)
    
    #增加互克类，【精灵弩手】遇【圣光骑士】攻击力增加50%
    def fightBuff(self, opponent, str1, str2):
        if opponent.name == '【圣光骑士】':
            self.fight = int(1.5*self.fight)
            print('『%s』【精灵弩手】对 『%s』【圣光骑士】说：“骑着倔驴又如何？你都碰不到我衣服。”'%(str1, str2))

#游戏类主类，上面的角色类是为它服务，附加在里面的
class Blood3Class:#类名一般大写注意
    #随机生成角色
    #【以下固定信息，不需每局都要初始化，所以放外面，不需放init中即可】
    myList = ['【狂血战士】','【森林箭手】','【光明骑士】','【独行剑客】','【格斗大师】','【枪弹专家】']
    enemyList = ['【暗黑战士】','【黑暗弩手】','【暗夜骑士】','【嗜血刀客】','【首席刺客】','【陷阱之王】']
    #把随机生成血量和攻击力与角色对应起来，用dict，定义两个dict 敌我信息
    #myInfo = {}
    #enemyInfo = {}
    #新角色生成通过方法类方法，不用再字典匹配了，此部分功能可注掉了
    
    #最终结果计分
    myScore = 0#【计分需累计，不是每一局重新初始化，所以放外面，不放init初始化函数中，放在类里，ini外，相当于类里的全局变量的一个角色，方法中使用也是通过self.】
    enemyScore = 0
    #n = 0

    def __init__(self):
        #随机选三个，用random.sample(seq,n)#列表，取的个数
        #【以下两步，每一局都要生成重新init初始化，所以放在初始化函数中，上面那些因为是类里固定不动信息，所以放外面了】
        #self.myRoles = random.sample(self.myList,3)
        #self.enemyRoles= random.sample(self.enemyList,3)
        #改为角色类生成的
        self.myRoles = []
        self.enemyRoles = []

        #【注意：原main函数中的调用函数过程，直接放在init初始化函数里，
        # 初始化函数就相当于主函数，自动第一时间默认执行】

        #以下要按顺序执行，注意，如：欢迎在前
        #游戏前导文
        self.welcome()
        #调生成角色类
        self.bornRole()#先生成角色 
        #调角色抱团互补类
        self.addBloodBuff()#【注意：角色已生成好，再判断角色是否相同，是通过方法的先后执行来实现的，#避免与初始值混淆】  
        #调用显示角色信息类
        self.show_role()
        #调用显示出场顺序类
        self.chooseOrder()
        #调用角色pk类
        self.pk_role()
        #显示终局结果
        self.showFinalResult()


    #游戏前导文字
    def welcome(self):
        print("=====欢迎开始游戏！！～～2019年1月24日 四=====")
        time.sleep(1)
        input("回车开始游戏")
    #随机生成血量和攻击方法
    # （【先粘过来，属性不用加self，后面报错时再调，
    # 此处不加self，因为用了return，其它函数调用的返回值结果，所以没用self放在类属性里】）
    '''
    def addBloodFight(self):
        blood = random.randint(100,180)
        fight = random.randint(30,50)
        return blood,fight
    '''
    #上面已改为在角色类中匹配，不需要随机指定用字典匹配了

    #随机生成角色
    def bornRole(self):
        '''
        myRoles = self.myRoles
        enemyRoles = self.enemyRoles
        myInfo = self.myInfo
        enemyInfo = self.enemyInfo

        #双方组装角色和对应血量攻击信息
        for i in range(3):
            myInfo[myRoles[i]] = self.addBloodFight()#上面方法返回值，即为所需的元组格式血量与攻击组合数据
            enemyInfo[enemyRoles[i]] = self.addBloodFight()#【调用方法加self.别忘了】
        '''
        #新功能类中匹配角色，上面字典匹配就不用了

        for i in range(3):
            self.myRoles.append(random.choice([Knight(),Assassin(),Bowman()]))
            self.enemyRoles.append(random.choice([Knight(),Assassin(),Bowman()]))
        #上面是随机生成三组三组对象实例，按随机顺序放入myInfo enemyInfo 列表中
        #print("我方随机born方法中11111111111self.myRoles"+str(self.myRoles[0].name+self.myRoles[1].name+self.myRoles[2].name))

    #补加抱团（随机生成的三个角色都一样）和互补（随机生成的三个角色都不一样）血量增加类
    def addBloodBuff(self):
        #set()生成去重后的数组
        myRNameList = [self.myRoles[0].name,self.myRoles[1].name,self.myRoles[2].name]#最后一个2写成了1，服务，查了很久
        #myRLen = len(set(self.myRoles))#【注意去重时只判断名字，否则，有可能血量和攻击力不同也算成我们都不同了】
        myRLen = len(set(myRNameList))
        #print("我方角报团方法中11111selfmyRoles"+str(self.myRoles[0].name+self.myRoles[1].name+self.myRoles[2].name))
        #print("我方角色报团方法中11111111111myRNameList"+str(myRNameList))
        
        enemyRNameList = [self.enemyRoles[0].name,self.enemyRoles[1].name,self.enemyRoles[2].name]
        #enemyRLen = len(set(self.enemyRoles))
        enemyRLen = len(set(enemyRNameList))

        #我方加血攻
        if myRLen == 1:#随机生成的角色全一样(放在for外面，先就知道是否一样，再给每一个加量)
            print("我方：我们都一样，团结就是力量，满血战斗！！加25%")
            for i in range(3):
                myBloodI = self.myRoles[i].blood
                myBloodI =  int(myBloodI*1.25)                
        if myRLen == 3:
            print("我方：我们各不同，互补大无边，攻击力全开！！加25%")
            for i in range(3):
                myFightI = self.myRoles[i].fight
                myFightI = int(myFightI*1.25)
            
        print("----------------")

        #敌方加血功
        if enemyRLen == 1:
            print("敌方：我们都一样，团结就是力量，满血战斗！！加25%")
            for i in range(3):
                enemyBloodI = self.enemyRoles[i].blood
                enemyBloodI = int(enemyBloodI*1.25)
        if enemyRLen == 3:
            print("敌方：我们各不同，互补大无边，攻击力全开！！加25%")
            for i in range(3):
                enemyFightI = self.enemyRoles[i].fight
                enemyFightI = int(enemyFightI*1.25)
                
    #显示角色信息类
    def show_role(self):

        myRoles = self.myRoles
        enemyRoles = self.enemyRoles
        #myInfo = self.myInfo
        #enemyInfo = self.enemyInfo
        #print("我方显示方法中11111111111111111myRoles"+str(myRoles[0].name+myRoles[1].name+myRoles[2].name))
        #print("我方显示方法中11111111111111111self.myRoles"+str(self.myRoles[0].name+self.myRoles[1].name+self.myRoles[2].name))
        # 展示我方的3个角色
        print('----------------- 角色信息 -----------------')
        print('我方人物：')
        for i in range(3):
            #print('%s 血量：%d 攻击：%d' % (myRoles[i],myInfo[myRoles[i]][0],myInfo[myRoles[i]][1]))
            #新功能非字典匹配，改为了myInfo enemyInfo 类实例对象列表
            print('%s 血量：%d 攻击：%d' % (myRoles[i].name,myRoles[i].blood,myRoles[i].fight))
        
        # 展示敌方的3个角色
        print('----------------- 角色信息 -----------------')
        print('敌方人物：')
        for i in range(3):
            #print('%s 血量：%d 攻击：%d' % (enemyRoles[i],enemyInfo[enemyRoles[i]][0],enemyInfo[enemyRoles[i]][1]))
            print('%s 血量：%d 攻击：%d' % (enemyRoles[i].name,enemyRoles[i].blood,enemyRoles[i].fight))
        input("请按回车继续.\n")#加一个输入互动，打断下，给用户控制进程

    #增加用户选三个角色出场顺序功能类
    def chooseOrder(self):

        myRoles = self.myRoles
        enemyRoles = self.enemyRoles

        #print("==旧排序==",myRoles)
        orderDict = {}
        for i in range(3):        
            order = int(input('请选择'+myRoles[i].name+'第几个出场？输入1,2,3'))#只需组我方，敌方不需要我来指定出场次序，电脑分配即可。
            #orderDict[order] = myRoles[i].name
            orderDict[order] = myRoles[i]#注意此处就不要把排序号对应值只加名字了，这回是对象整体，在角色类中匹配的，不是在开头的字典中匹配的。
        
        #打印我方出场顺序
        myRoles = []
        #按新排序加到 空列表中即可替换
        for i in range(1,4):#为什么改为1开始，因为orderDict的键是1,2,3从1开始对应起来
            myRoles.append(orderDict[i])

        #以下两行从order字典取和从根据排序字典新排的list取，都可以
        #print("我方角色出场顺序：%s %s %s " % (orderDict[1],orderDict[2],orderDict[3]))#注意按key取，key是1，2，3,不是索引
        print("我方角色出场顺序：%s %s %s " % (myRoles[0].name,myRoles[1].name,myRoles[2].name))#列表按索引(python里也叫偏移量)取从0开始
        print("敌方角色出场顺序：%s %s %s " % (enemyRoles[0].name,enemyRoles[1].name,enemyRoles[2].name))
        #print("敌方角色出场顺序：%s %s %s " % (enemyRoles[0],enemyRoles[1],enemyRoles[2]))
    #双方PK类
    def pk_role(self):
        global myScore
        global enemyScore
        #global n
        #n = self.n
        #【总结：此处两个变量需累加，需要用global把局部计算结果提升到全局进行累加，
        #不可直接用self.myScore，类实例相当于复制了一个新属性，每一个实例不会影响到类，所以不会累加回去】
        #下面两行是指定初始值为全局属性score 0,在for遍历计算中每战一局累加一次。
        #】
        myScore = self.myScore
        enemyScore = self.enemyScore

        myRoles = self.myRoles
        enemyRoles = self.enemyRoles
        #myInfo = self.myInfo
        #enemyInfo = self.enemyInfo

        #首先是打三局，每局传入一个角色开战
        for i in range(3):#打三局
            #战前展示战斗信息 第i局
            print('\n----------------- 【第%d局】 -----------------' % i)
            #赛前按规则增加buff
            self.myRoles[i].fightBuff(self.enemyRoles[i],'我方','敌方')
            #【一个实例对象（myRoles是一个对象的list，见bore方法）.fightBuff调它的方法，传参。
            # 当敌方的i与我方的i刚好匹配到克制关系时即攻击力按规则变化】
            self.enemyRoles[i].fightBuff(myRoles[i],'敌方','我方')
            #相互对战，敌人的也要设置。双双设置

            #n = n+1
            #print(myInfo)
            #{'【光明骑士】': (113, 31), '【格斗大师】': (162, 49), '【独行剑客】': (104, 34)}
            #角色名
            #myRole = myRoles[i]#【myRoles是新排序的，这里取新排序的第1,2,3位，即实现了人工选的第1,2,3位先出场】
            #enemyRole = enemyRoles[i]
            myRole = myRoles[i].name
            enemyRole = enemyRoles[i].name
            #血量
            #myBlood = myInfo[myRoles[i]][0]
            #myFight = myInfo[myRoles[i]][1]
            myBlood = myRoles[i].blood
            myFight = myRoles[i].fight
            #攻击力
            #enemyBlood = enemyInfo[enemyRoles[i]][0]
            #enemyFight = enemyInfo[enemyRoles[i]][1]
            enemyBlood = enemyRoles[i].blood
            enemyFight = enemyRoles[i].fight

            print('玩家角色：%s vs 敌方角色：%s ' %(myRole,enemyRole))
            print('%s 血量：%d  攻击：%d' %(myRole,myBlood,myFight))
            print('%s 血量：%d  攻击：%d' %(enemyRole,enemyBlood,enemyFight))
            print('--------------------------------------------')
            input('请按回车键继续。\n')

            while myBlood > 0 and enemyBlood > 0 :#注意这里不用剩余血量，因为血量的全局变量是会覆盖到最后的
                myBlood = myBlood - enemyFight
                enemyBlood = enemyBlood - myFight
                myRs = '你发起了攻击，【玩家】剩余血量 %d ' % myBlood
                enemyRs = '敌人向你发起了攻击，【敌人】的剩余血量 %d ' % enemyBlood
                print(myRs)
                print(enemyRs)
                print("----------------")
                time.sleep(1)
            #一局循环结束，显示结果
            print(self.show_result(myBlood,enemyBlood,myScore,enemyScore))#【计分移到另一方法中了，此处score传参过去，相当于在此地计算一样的】

        
    def showFinalResult(self):
        global myScore#只是取用全局变量其实不用加global，加上也没错，最好加上吧，确定一下，免得下面再有需要局部计算的。
        global enemyScore
        input('\n点击回车，查看比赛的最终结果\n')
        print("===【战局公布】===")
        #print("nnnnnnnnn"+str(n))
        #print("mmmmmmmmmmmmmmmmmmmmmyScore"+str(myScore))
        #print("eeeeeeeeeeeeeeeeeeeeeenemyScoree"+str(enemyScore))
        #显示最终结果
        if myScore > enemyScore:
            print("我以 %d : %d 战胜了敌方" % (myScore,enemyScore))
        elif myScore < enemyScore:
            print("敌人以 %d : %d 击败了我" % (enemyScore,myScore))
        elif myScore == enemyScore:
            print("我和敌方 %d : %d 平" % (myScore,enemyScore))

    #计分并展示单局结果类
    def show_result(self, myBlood,enemyBlood,myScoreParam,enemyScoreParam):
        global myScore #计算结果累加到全局，所以需加global
        global enemyScore
        #【总结：此处两个变量需累加，需要用global把局部计算结果提升到全局进行累加，
        #不可直接用self.myScore，类实例相当于复制了一个新属性，每一个实例不会影响到类，所以不会累加回去】
        #上面是把变量声明为全局，下面是给score取初始值，开始累加，累加结果会自动变为全局变量（因为加了global），
        #在取用的地方直接取即可。】
        #myScore = self.myScore #这样不行，是取单次累加成绩了，要三局两胜都取，还是要在上一个函数for传值过来计算累加
        #enemyScore = self.enemyScore
        myScore = myScoreParam#所以用下面这种，参数名字和myScore重名，影响加blobal，所以换名字了，这里它表示for一个战局里的一次计分参数，而不是全局变量myScore
        enemyScore = enemyScore#【注意此处的赋值，这两步调了好久，很容易出错，pk函数里的值是初始值0，这里的是上一次的累加结果，不理解的话，想象下把这块分出来的方法再贴回for循环里就明白了】
        
        if myBlood >0 and enemyBlood <=0: 
            myScore = myScore + 1
            return '敌人死翘翘了，这局你赢了'
        elif myBlood <=0 and enemyBlood >0:
            enemyScore = enemyScore + 1
            return '悲催，这局敌人把你干掉了！'
        else:
            return '哎呀，这局你和敌人同归于尽了！'

newgame = Blood3Class()



#思路：第一步v1.0，【函数移到类里变成一个整体函数包】
#【1)建一个类，把全局变量放在类属性里；】
#【2)把函数搬进来，传self参数; 使用时用self.属性。】
#【3）原main主函数中的调用分函数语句，放在__init__()初始函数里】
#【4）计分score的局部计算全局累加，注意在方法中声明为global,
# 取初始值时self.score取初始0，三局两胜计算时取值为上一次的循环结果不是self.score了，注意】
#调试跑通达到和blood2.py一样效果即可。
#欣慰吧～～终于可以自如使用类封装了！～划时代的进步！～2019/1/23 三 于风变

#第二步v2.0 写角色类，即原来的角色血量和攻击力都是用的一个随机产生的，此处给每一个单独加特定的
#写三个角色类，生成不同的属性，
# 加克制关系（加角色生成类里，因创建角色的时候就可以确定条件并完成计算了），在show_role里面取用

#第三步作业：补加方法：当随机生成的角色全相同时（抱团）血量增加25%，全不同时（互补）攻击力加25%
#判断一样不一样用set()长度判断，set()生成去重后的列表。注意取实例对象的name，#血量和攻击力混着都是不同的
#（加在blood3Class游戏类里，因为只有随机生成后，才能确定条件根据条件计算。
# 【方法加在哪，完全凭需要，看到没，重点啊】）
#【（改变血量是通过改变类属性即可完成。类方便吧。）
#所以总结：
# ***==你看类能很方便的在一个方法里改变属性给其它方法做到同步，不用思考的，所以是面向对象接口。
# 而函数是要思考过程，流程，每个值的return 再给其它什么在什么地点什么时候用的。体会到不同了吗？==***】
#==本例的用意：【灵活运用类，在后续灵活加入改造，
# 灵活（包括opponent外部传参改内部方法那里等）修改类的元素（无非就是属性、方法），
# 来完善自己的功能==】
#init函数中的方法调用要按顺序注意，如：欢迎在前。
#【注意：角色已生成好，再判断角色是否相同，是通过方法的先后执行来实现的，#避免与初始值混淆】
# 之前的随机指定键值关系用字典匹配大法，本例替换为了封装单个角色类来指定，并丰富了下。