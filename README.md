# EasyClass
超星刷课软件
版本：0.0.2
作者：Hugo

声明：
	本品是一款模拟人对网页进行操作的软件，不会加速视频播放等破坏网页播放规则或者对安全造成影响的行为。
	本程序仅限于学习交流，禁止一切商务使用。

版本更新：
	针对超星学习通网页变动更新操作方式；
	修复了会重复开始同一个视频的bug；
	修复了课程选择会跳转到其他课程的bug；

代码开发说明：
	本程序使用selenium模块进行开发，请安装python解释器并下载selenium。
    主程序中包含一个EasyClass类，可以作为单独库导入（记得复制一份然后改名）

使用说明：
	启动程序：在main文件夹下运行main.exe。
	本产品支持最新版本火狐浏览器，如果您的电脑上没有火狐浏览器，请安装。
	产品驱动下载地址：https://github.com/mozilla/geckodriver/releases，请选择最新版下载。
	在登录之前请先登录您的学习通，复制第一节课的网址。
	该程序针对老版本超星网页设计，使用时请按照示例将网址删减到规定样式。
		当前网址：https://mooc1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245&mooc2=1&cpi=157710188&openc=8983c8940b12e650265152adbd0aeb6c
		删除的部分：&mooc2=1&cpi=157710188&openc=8983c8940b12e650265152adbd0aeb6c（即将&mooc2=后面的数据全部删除）
		老版本网址：https://mooc1.chaoxing.com/mycourse/studentstudy?chapterId=398481847&courseId=217666369&clazzid=39610013&enc=1812c2df5429653b1f6ed82782730245
	本程序需要您输入用户名和密码，本人承诺该程序中不含有盗取您账号和密码的行为。
    在输入账号和密码之后，Firefox浏览器会自动弹出，请不要担心。如果您是第一次使用firefox浏览器，可能会导致程序启动失败，届时请关闭程序重启即可
    因为网速问题，可能会导致视频时长获取失败，请保证网络通畅。

火狐浏览器驱动下载地址：
	https://github.com/mozilla/geckodriver/releases