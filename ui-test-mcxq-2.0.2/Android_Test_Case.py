import shutil
from airtest.core.api import *
from Aritest_Convenient import Aritest_Convenient
from Get_image import Get_image


class Mk_Android_test():
    def __init__(self,phone_number,user_state=1):
        #user_state ：： 0-历史用户，1-新用户
        self.user_state = user_state
        self.phone_number = phone_number


    shutil.rmtree("/Users/panshuhuai/Documents/ui_log")
    os.mkdir("/Users/panshuhuai/Documents/ui_log")
    auto_setup(__file__, logdir=True,
               devices=["android://127.0.0.1:5037/CWM0222127002637?cap_method=MINICAP&touch_method=MAXTOUCH&", ])
    start_app('com.papet.cpp')

    @staticmethod
    def App_initialization():
        #手机APP初始化回归（隐私弹窗协议）
        img_road = Get_image("android_img/App_initialization")
        sleep(5)
        check_pop = Aritest_Convenient.check_element(img_road.img_name("用户协议弹窗"),sleep_time=5)
        if check_pop != False:
            pos = Aritest_Convenient.check_element(img_road.img_name("隐私协议"),no_pass=True)
            if pos != False:
                Aritest_Convenient.touch_sleep(pos)
                Aritest_Convenient.check_element(img_road.img_name("隐私协议正文"),threshold=0.75,sleep_time=2)
                Aritest_Convenient.touch_sleep(img_road.img_name("隐私协议返回按钮"))
            else:
                pass
            pos = Aritest_Convenient.check_element(img_road.img_name("用户协议"),threshold=0.75,no_pass=True)
            if pos != False:
                Aritest_Convenient.touch_sleep(pos)
                Aritest_Convenient.check_element(img_road.img_name("用户协议正文"))
                Aritest_Convenient.touch_sleep(img_road.img_name("用户协议返回按钮"))
            else:
                pass
            pos = Aritest_Convenient.check_element(img_road.img_name("协议同意按钮"))
            if pos != False:
                Aritest_Convenient.touch_sleep(pos)
            else:
                Aritest_Convenient.touch_sleep((620,1822))

    def Mk_log_in(self):
        #手机启动登录页，输入手机号码，填写验证码
        user_phone = self.phone_number
        img_road = Get_image("android_img/mk_log_in")#载入路劲
        Aritest_Convenient.check_element(img_road.img_name("输入手机号码"))
        Aritest_Convenient.touch_sleep(img_road.img_name("输入手机号码"))
        Aritest_Convenient.input_text(str(user_phone))
        pos = Aritest_Convenient.check_element(img_road.img_name("同意协议圆点按钮"),ex_touch=(98,1740))
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)
        pos=Aritest_Convenient.check_element(img_road.img_name("获取验证码按钮"),no_pass=True)
        Aritest_Convenient.touch_sleep(pos,sleep_time=2)
        Aritest_Convenient.input_text("123456") #验证码获取
        sleep(2)


    def New_user_pk_page(self):
        #新手注册+新手引导+
        #需要使用一个全新的用户号码执行此用例
        if self.user_state == 0:
            return False
        img_road = Get_image("android_img/New_user_pk_page")
        pos = Aritest_Convenient.check_element(img_road.img_name("用户头像上传"),sleep_time=2,ex_touch=(607,884))#验证上传头像
        if pos == False:
            snapshot('用户头像上传',msg="'用户头像上传'--图片与预期不符，请更换用例UI图片")
        else:
            Aritest_Convenient.touch_sleep(pos)#点击上传头像，进入拍摄页

        pos = Aritest_Convenient.check_element(img_road.img_name('手机相机授权图标'),sleep_time=2,ex_touch=(257,1126))#手机授权
        if pos == False:
            snapshot('手机相机授权图标',msg='手机相机授权图标-图与预期不符，请及时更换')
        else:
            Aritest_Convenient.touch_sleep(pos)#点击授权手机权限
        pos = Aritest_Convenient.check_element(img_road.img_name('系统相册授权弹窗允许'),ex_touch=(918,2550))
        if pos ==False:
            pos = (918,2550)
        Aritest_Convenient.touch_sleep(pos,sleep_time=2)#授权相机权限
        Aritest_Convenient.touch_sleep(pos,sleep_time=2)#授权开启麦克风
        pos = Aritest_Convenient.check_element(img_road.img_name('手机媒体权限允许'),ex_touch=(884,2553))#授权开启相册
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)
        pos = Aritest_Convenient.check_element(img_road.img_name('拍摄页相册图标'),ex_touch=(239,2285))
        if pos == False:
            snapshot('拍摄页相册图标', msg='拍摄页相册图标-图与预期不符，请及时更换')
        else:
            Aritest_Convenient.touch_sleep(pos)#打开手机相册
        if Aritest_Convenient.touch_sleep(img_road.img_name('相册中的测试图片')) == False:
            Aritest_Convenient.touch_sleep((759,1074))#选中相册素材即可
        pos = Aritest_Convenient.check_element(img_road.img_name('编辑头像保存按钮'),ex_touch=(1098,236))
        if pos == False:
            snapshot('编辑头像保存按钮', msg='编辑头像保存按钮-图与预期不符，请及时更换')
        else:
            Aritest_Convenient.touch_sleep(pos)#点击编辑头像保存按钮
        if Aritest_Convenient.touch_sleep(img_road.img_name('输入宠物昵称')) == False:
            Aritest_Convenient.touch_sleep((183,1422))
        Aritest_Convenient.input_text("小猫猫")
        pos = Aritest_Convenient.wati_element(img_road.img_name('注册完成按钮'),timeout=5)
        Aritest_Convenient.touch_sleep(pos)#注册完成按钮点击
        Aritest_Convenient.wati_element(img_road.img_name('新手引导弹窗'),timeout=6)#等待新手弹窗展示
        Aritest_Convenient.check_element(img_road.img_name('新手引导跳过按钮'))
        pos = Aritest_Convenient.wati_element(img_road.img_name('新手引导弹窗按钮'),timeout=6)
        Aritest_Convenient.touch_sleep(pos)#点击我知道了
        pos = Aritest_Convenient.check_element(img_road.img_name('动效单击'))
        if pos == False:
            pos = Aritest_Convenient.check_element(img_road.img_name('动效单击'))
            if pos == False:
                pos = (80,864) #若识别不到动效，则点击空白处跳过
        Aritest_Convenient.check_element(pos)#点击关闭动效
        pos = Aritest_Convenient.check_element(img_road.img_name('新手引导pk矮油'))
        if pos != False:
            Aritest_Convenient.check_element(img_road.img_name('新手引导pk亦菲'))
        else:
            pos = Aritest_Convenient.check_element(img_road.img_name('新手引导pk亦菲'))
            if pos == False:
                Aritest_Convenient.touch_sleep((511,1644))#随机选一个点击
            else:
                Aritest_Convenient.touch_sleep(pos)#点识别到的PK
        pos = Aritest_Convenient.check_element(img_road.img_name('新手奖励开心收下'))
        Aritest_Convenient.check_element(pos)#点击开心收下
        Aritest_Convenient.check_element(img_road.img_name("引导加入比赛弹窗"),sleep_time=3)
        pos = Aritest_Convenient.check_element(img_road.img_name('引导加入比赛弹窗好的'),ex_touch=(603,1854))
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)
        Aritest_Convenient.check_element(img_road.img_name('加入比赛引导'))
        pos = Aritest_Convenient.check_element(img_road.img_name('引导加入比赛弹窗好的'), ex_touch=(426, 1608))
        if pos != False:
            Aritest_Convenient.check_element(pos)#点击好的
        pos = Aritest_Convenient.check_element(img_road.img_name('参加比赛现在加入'),no_pass=True)
        Aritest_Convenient.touch_sleep(pos)#
        Aritest_Convenient.check_element(img_road.img_name("新手引导余额确认"))
        pos = Aritest_Convenient.check_element(img_road.img_name('参赛关闭按钮'))
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)
        pos = Aritest_Convenient.check_element(img_road.img_name('比赛详情页返回按钮'))
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)


    @staticmethod
    def Pk_review_page():
    #从比赛页进入审评页，评选10次至展示到三文鱼奖励弹窗出现后关闭
        img_road = Get_image("android_img/Pk_review_page")  # 载入路劲
        pos = Aritest_Convenient.wati_element(img_road.img_name("未选中pk分类"),timeout=5)
        if pos == False:
            pos = (180,2504)
        Aritest_Convenient.touch_sleep(pos)
        if isinstance(pos,tuple):
            for i in range(11):
                if i % 2 == 0:
                    Aritest_Convenient.touch_sleep((655,762))#点击上方参赛作品
                    sleep(3)
                else:
                    Aritest_Convenient.touch_sleep((723,1890))#点击下方参赛作品
                    sleep(3)
            if Aritest_Convenient.check_element(img_road.img_name("三文鱼奖励弹窗"),no_pass=True) != False:
                Aritest_Convenient.touch_sleep((618,1901))#点击弹窗关闭按钮
        else:
            snapshot("review page",msg="pk评审页进入时出现异常")\


    @staticmethod
    def Tribal_warfare_page():
    #部落战争参赛页，主流程回归
        img_road = Get_image("android_img/Tribal_warfare_page")
        pos = Aritest_Convenient.check_element(img_road.img_name('未选中底部战争分类'))
        if pos != False:
            Aritest_Convenient.touch_sleep(pos)#点击进入部落战争分类
        pos = Aritest_Convenient.check_element(img_road.img_name('战争首页现在加入'))
        Aritest_Convenient.get_height_position_button(pos)

if __name__ == '__main__':
    test_case = Mk_Android_test(phone_number='16200000006',user_state=1,)
    test_case.App_initialization()
    test_case.Mk_log_in()
    test_case.New_user_pk_page()
    test_case.Pk_review_page()