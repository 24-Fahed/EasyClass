from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from re import findall
import os


# https://mooc1.chaoxing.com/mycourse/studentstudy?chapterId=443991288&courseId=223543911&clazzid=52846586&enc=a6610ceda146c4bba791421adedaa3d6

class EasyClass(object):
    def __init__(self, classurl, userID, passwd):
        # 创建浏览器驱动
        self.drive = webdriver.Firefox()
        # 创建网址组装格式
        # self.demo = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId={}&courseId={}&clazzid={}&enc={}'.format('', '', '', self.createwebdemo(classurl))
        self.classurl = classurl
        self.userID = userID
        self.passwd = passwd
        self.allclass = 0
        self.class_xpath_list = []
        self.flage = True
        # 是否可以开始播放视频，如果不能为False，可以为True
        self.pagedone = False
        self.classnum = 0
        # 是否允许切换视频
        self.switchclass = False

    def createwebdemo(self, classurl):
        # url = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245'
        ens = findall('enc=(.*)', classurl)
        # print(ens)
        return ens

    def log_in(self):
        '''
        使用模块登陆学习通
        :param drive:浏览器驱动
        :param url:登陆的网址
        :return:操作后的（已登陆）驱动
        '''
        self.drive.get(self.classurl)
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
        return 0

    def start_video(self):
        '''
        开始视频播放
        :return: NONE
        '''
        # 切换frame
        self.drive.execute_script("window.scrollBy(0,1000)")
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
        sub_butt = self.drive.find_element_by_id("videoquiz-submit")
        # 点击提交按钮
        sub_butt.click()
        return

    def check_cycle(self):
        '''/html/body/div[4]/div/div[1]/span/div/div/ul//label/input'''
        '''
        该循环用来检测视频中是否出现答题环节
        :return:NONE
        '''
        # qustion = self.drive.find_element_by_class_name("tkItem_title")
        # quiz = qustion.find_element_by_class_name("ans-videoquiz-title")
        # print(quiz.text)
        # opt = qustion.find_elements_by_xpath("/html/body/div[4]/div/div[1]/span/div/div/ul/li/label/input")
        # 上面为老代码
        # 超星更新，将答题页面修改为一个iframe

        qustion = self.drive.find_element_by_class_name("tkItem")
        quiz = qustion.find_element_by_class_name("tkItem_title")
        print(quiz.text)
        # opt = qustion.find_elements_by_xpath("/html/body/div/div[4]/div/div[1]/span/div/div/div/div[2]/div/ul/li[1]/label/span/input")
        opt = qustion.find_elements_by_xpath(
            "/html/body/div/div[4]/div/div[1]/span/div/div/div/div[2]/div/ul//label/span/input")

        print(opt)
        for opt_t in opt:
            value = opt_t.get_attribute("value")
            if value == "true":
                opt_t.click()
                self.submit(qustion)

    def get_time(self):
        sleep(10)
        # drive.find_elements_by_xpath()
        # /html/body/div/div[4]/div/div[5]/div[4]/span[2]
        # long = self.drive.find_elements_by_xpath('/html/body/div[4]/div/div[5]/div[4]/span[2]')
        long = self.drive.find_element_by_xpath("/html/body/div/div[4]/div/div[5]/div[4]/span[2]")
        print(long.get_attribute('outerHTML'))
        # selenium更新，指定一个标签的时候会直接返回一个对象，不会返回列表了

        strlong = long.get_attribute("textContent")
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
        切换到指指定视频
        :param class_xpath_list:
        :param num:
        :return:
        '''
        # 如果课程已经刷完
        if self.classnum == self.allclass:
            self.flage = False
            return

        # 切换回主界面
        self.drive.switch_to.default_content()
        # 找到指定课程xpath
        xpath_next = self.class_xpath_list[self.classnum - 1]

        b = self.drive.find_elements_by_xpath(xpath_next)
        # print(b)
        b[0].click()
        print("切换到课程：", self.drive.find_elements_by_xpath(xpath_next)[0].get_attribute('textContent'))
        print("剩余：", self.allclass - self.classnum, "节课")

    def getClassnum(self):
        '''
        返回剩余课程数量
        :return:
        '''
        return self.classnum

    def setClassnum(self):
        '''
        剩余课程量
        :return:
        '''
        # self.classleft = self.allclass - int(input("请输入课程序号"))
        self.classnum = int(input("请输入课程序号"))


if __name__ == "__main__":
    print("欢迎使用EasyClass | V 0.0.2")
    print("作者：Hugo")
    print("正在检测系统环境：")
    print("根据下面的提示完成相应操作，您就可以使用本程序进行刷课了")
    print("====================================================================")
    exam = 'https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245'
    userID = input("请输入用户名：")
    passwd = input("请输入密码：")
    print("网址示例：", exam)
    url = input("请输入起始网址")
    # https://mooc1-1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245
    ec = EasyClass(url, userID, passwd)
    ec.log_in()
    # 获取课程列表
    ec.get_class_xpath()
    ec.setClassnum()
    print("选中课程：", ec.getClassnum())
    # 开始视频播放
    # while ec.flage != False:
    #     try:
    #         sleep(5)
    #         ec.go_to_videoPage("c2")
    #         sleep(5)
    #         ec.start_video()
    #     except Exception as e:
    #         print(e)
    #         ec.go_to_videoPage("c1")
    #         sleep(3)
    #         ec.start_video()
    #     try:
    #         time = ec.get_time()
    #         if time == 0:
    #             print("重新尝试获取时长")
    #             time = ec.get_time()
    #         else:
    #             ec.start_check(time)
    #             ec.next_video()
    #     except Exception as ee:
    #         print(ee)

    # 开始视频播放
    vidio_tag_list = ['c1', 'c2']
    while ec.flage != False:
        # 定位到标签并开始视频
        try:
            # 切换视频到指定位置
            if ec.switchclass == False:
                try:
                    ec.next_video()
                    ec.switchclass = True
                except:
                    continue

            if ec.pagedone == False:
                for i in vidio_tag_list:
                    sleep(5)
                    try:
                        ec.go_to_videoPage(i)
                        sleep(5)
                        ec.start_video()
                        sleep(5)
                        ec.pagedone = True
                        break
                    except:
                        print("尝试切换标签")
                        continue
        except:
            print("视频所在页面标签定位错误")
            continue

        # 开始视频播放并检测是否进入下一节
        try:
            time = ec.get_time()
            if time == 0:
                # 尝试重新获取时间
                print("重新获取时常")
                time = ec.get_time()
            else:
                ec.start_check(time)
                ec.pagedone = False
                ec.switchclass = False
                ec.classnum += 1
                ec.next_video()
        except Exception as err:
            print("未知错误")
            print(err)

    os.system('pause')