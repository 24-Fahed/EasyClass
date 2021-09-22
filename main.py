from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from re import findall
import os

class EasyClass(object):
    def __init__(self, classurl, userID, passwd):
        # 创建浏览器驱动
        self.drive = webdriver.Firefox()
        # 创建网址组装格式
        self.demo = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId={}&courseId={}&clazzid={}&enc={}'.format('', '', '', self.createwebdemo(classurl))
        self.userID = userID
        self.passwd = passwd
        self.classleft = 0
        self.allclass = 0
        self.class_xpath_list = []
        self.flage = True


    def createwebdemo(self, classurl):
        # url = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245'
        ens = findall('enc=(.*)', classurl)
        # print(ens)
        return ens

    def log_in(self, url):
        '''
        使用模块登陆学习通
        :param drive:浏览器驱动
        :param url:登陆的网址
        :return:操作后的（已登陆）驱动
        '''
        self.drive.get(url)
        sleep(1)
        content = self.drive.find_element_by_id("phone")
        password = self.drive.find_element_by_id("pwd")
        button = self.drive.find_element_by_id("loginBtn")
        
        content.send_keys(self.userID)
        password.send_keys(self.passwd)
        input("如果有验证码，请先进行人工识别，输入完成后，请回命令行按回车")
        sleep(3)
        button.click()
        return self.drive

    def go_to_videoPage(self, tag):
        '''
        自动检测视频播放页面，并跳转
        :param tag: 跳转视频播放页面并播放视频
        :return:NONE
        '''
        self.drive.switch_to.default_content()
        js = 'document.getElementsByClassName("{}")[0].click()'.format(tag)
        print(js)
        self.drive.execute_script(js)

    def start_video(self):
        '''
        开始视频播放
        :return: NONE
        '''
        # 切换frame
        self.drive.switch_to.frame('iframe')

        self.drive.switch_to.frame(0)
        sleep(2)

        button = self.drive.find_elements_by_xpath('//div[@id="video"]/button')
        print(button[0].text)
        button[0].click()

    def submit(self, qustion):
        '''
        提交答案按钮
        :param qustion: 视频中问题的标签
        :return: NONE
        '''
        sleep(1)
        # 寻找提交按钮
        sub_butt = qustion.find_element_by_class_name("ans-videoquiz-submit")
        # 点击提交按钮
        sub_butt.click()
        return

    def check_cycle(self):
        '''<selenium.webdriver.firefox.webelement.FirefoxWebElement (session="758bdc5d-314a-43c1-974c-3b528182ff47", element="f81fa45c-5ec1-45e8-9da6-30c65727ad6c")>'''
        '''<selenium.webdriver.firefox.webelement.FirefoxWebElement (session="758bdc5d-314a-43c1-974c-3b528182ff47", element="3e17dffa-5afe-4c32-b6a1-9f76325828be")>'''
        '''/html/body/div[4]/div/div[1]/span/div/div/ul/li[1]/label/input'''
        '''
        该循环用来检测视频中是否出现答题环节
        :return:NONE
        '''
        qustion = self.drive.find_element_by_class_name("x-component")
        quiz = qustion.find_element_by_class_name("ans-videoquiz-title")
        print(quiz.text)
        opt = qustion.find_elements_by_xpath("/html/body/div[4]/div/div[1]/span/div/div/ul/li/label/input")
        print(opt)
        for opt_t in opt:
            value = opt_t.get_attribute("value")
            if value == "true":
                opt_t.click()
                self.submit(qustion)

    def get_time(self):
        sleep(20)
        # drive.find_elements_by_xpath()
        long = self.drive.find_elements_by_xpath('/html/body/div[4]/div/div[5]/div[4]/span[2]')

        strlong = long[0].get_attribute("textContent")
        min = int(strlong[0: strlong.index(":")])
        sec = int(strlong[strlong.index(":") + 1:])
        print("时常：", min, ':', sec)
        sumlong = min * 60 + sec
        return sumlong

    def start_check(self, t):
        '''
        开启检查进程
        :param t: 视频总时长
        :return:
        '''
        t = int(t / 5)
        for _ in range(t):
            # process2 = multiprocessing.Process(target=check_cycle)
            # process2.start()
            try:
                self.check_cycle()
            except Exception as r:
                print("暂时未发现目标", _, r)
            sleep(5)
            # 测试代码+++++++++++++++++++
            # break

    def get_class_xpath(self):
        '''
        获取课程列表
        :return: 返回列表，包含所有课程的xpath
        '''
        try:
            charp_list = self.drive.find_elements(By.XPATH, '//*[@id="coursetree"]/div')
            xpath_demo = '//*[@id="coursetree"]/div[{}]/div/h4/a'
            xpath_list = []
            for numP in range(len(charp_list)):
                xpath_demo2 = '//*[@id="coursetree"]/div[{}]/div[{}]/h4/a'
                classjsNum = len(self.drive.find_elements_by_xpath(xpath_demo.format(numP + 1)))
                for numC in range(classjsNum):
                    xpath_new2 = xpath_demo2.format(numP + 1, numC + 1)
                    xpath_list.append(xpath_new2)
            if len(xpath_list) == 0:
                raise TimeoutError
            print('一共有%d节课', len(xpath_list))
            self.allclass = len(xpath_list)
            self.class_xpath_list = xpath_list

        except Exception as e:
            print(e)
            print("获取出错，5秒后重试")
            sleep(5)
            self.get_class_xpath()


    def next_video(self):
        '''
        播放下一条视频
        :param class_xpath_list:
        :param num:
        :return:
        '''
        self.classleft -= 1
        if self.classleft == 0:
            self.flage = False
        # 切换回主界面
        self.drive.switch_to.default_content()
        #print(self.classleft)
        #print(self.allclass - self.classleft)
        #print(self.class_xpath_list)
        xpath_next = self.class_xpath_list[self.allclass - self.classleft] # 出错
        # print(xpath_next)
        # print(xpath_next)
        b = self.drive.find_elements_by_xpath(xpath_next)
        # print(b)
        b[0].click()
        print("切换到课程：", self.drive.find_elements_by_xpath(xpath_next)[0].get_attribute('textContent'))
        print("剩余：", self.classleft, "节课")

    def getClassnum(self):
        '''
        返回剩余课程数量
        :return:
        '''
        return self.allclass - self.classleft

    def setClassnum(self):
        '''
        剩余课程量
        :return:
        '''
        self.classleft = self.allclass - int(input("请输入课程序号"))






if __name__ == "__main__":
    print("欢迎使用刷客软件 | V 0.0.1")
    print("作者：Hugo")
    print("根据下面的提示完成相应操作，您就可以使用本程序进行刷课了")
    print("====================================================================")
    exam = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245'
    userID = input("请输入用户名：")
    passwd = input("请输入密码：")
    print("网址示例：", exam)
    url = input("请输入起始网址")
    #https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245
    ec = EasyClass(url, userID, passwd)
    ec.log_in(url)
    # 获取课程列表
    ec.get_class_xpath()
    ec.setClassnum()
    print("选中课程：", ec.getClassnum())
    # 开始视频播放
    while ec.flage != False:
        try:
            sleep(5)
            ec.go_to_videoPage("c2")
            sleep(5)
            ec.start_video()
        except Exception as e:
            print(e)
            ec.go_to_videoPage("c1")
            sleep(3)
            ec.start_video()
        try:
            time = ec.get_time()
            if time == 0:
                print("重新尝试获取时长")
                time = ec.get_time()
            else:
                ec.start_check(time)
                ec.next_video()
        except Exception as ee:
            print(ee)

    os.system('pause')