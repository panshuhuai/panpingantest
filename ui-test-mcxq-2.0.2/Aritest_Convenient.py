import airtest.core.api
import airtest.core.cv
from airtest.core.api import *


class Aritest_Convenient():

    sleep_times = 1

    @staticmethod
    def touch_sleep(el,times=1,sleep_time=sleep_times,rgb=False,threshold=0.85):
        #点击事件的封装
        str_el = el
        element = Template(el,rgb=rgb,threshold=threshold)
        if isinstance(el,tuple) == True:
            #为元祖（坐标）则直接点击元素，不做校验
            touch(el,times=times)
            sleep(sleep_time)
            return element
        if isinstance(element,Template) == True and isinstance(el,tuple) != True:
            pos = exists(element)
            if pos == False:
                return False
            else:
                touch(pos)
                sleep(sleep_time)
                return pos

    @staticmethod
    def check_element(el,ex_touch=None,no_pass=False,sleep_time=1,rgb=False,threshold=0.85):
        #检查元素是否存在可用，若不在则可输入固定坐标实现跳过检查的点击
        sleep(sleep_time)
        element = None
        if isinstance(el,str):
            element = Template(el,rgb=rgb,threshold=threshold)
        if isinstance(el,tuple):
            touch(el)
        if no_pass == False and isinstance(element,Template):
            pos = exists(element)
            if ex_touch != None and pos == False:
                touch(ex_touch)
                return False
            else:
                pass
            return pos
        if no_pass == True and isinstance(element,Template):
            pos = assert_exists(element)
            return pos

    @staticmethod
    def input_text(input_text, enter=False, sleep_time=1):
        # 输入文本内容
        # input_text:: 输入的文字
        # enter::是否需要换行,默认为false-不换行
        # sleep_time::等待事件
        input_texts = str(input_text)
        try:
            text(text=input_texts, enter=enter)
            sleep(sleep_time)
        except:
            assert AssertionError("输入文字: %s 异常" % (input_text))

    @staticmethod
    def get_height_position_button(parameter, parameter_x=0, parameter_y=0):
        # 通过某元素位置，后调齐高低或水平位置，点击目标(需要减，请传入负数)
        if isinstance(parameter, airtest.core.api.Template):
            parameter = exists(parameter)
        button_parameter_x = parameter[0]
        button_parameter_y = parameter[1]
        button_parameter_list = []
        button_parameter_list.append(button_parameter_x + parameter_x)
        button_parameter_list.append(button_parameter_y + parameter_y)
        parameter_button = tuple(button_parameter_list)
        return parameter_button

    @staticmethod
    def touch_swipe(s_el, e_el=None, vector=None, sleep_time=1,rgb=False,threshold=0.85):
        # 点击定位后滑动至下一定位
        # start_element : 起始定位图片,必须使用airtest.core.api.Template格式图片元素
        # 终点参数1 end_selement : 拖动终点定位的airtest.core.api.Template格式图片元素
        #  终点参数2 vector : 终点坐标,如(100,200)
        # sleep_time :完成拖动后的等待时间
        start_element = Template(s_el,rgb=rgb,threshold=threshold)
        end_selement = Template(e_el,rgb=rgb,threshold=threshold)
        time.sleep(sleep_time)
        if end_selement != None:
            swipe(v1=start_element, v2=end_selement)
            time.sleep(sleep_time)
        if vector != None:
            swipe(v1=start_element, vector=vector)
            time.sleep(sleep_time)
        else:
            raise AssertionError("touch_swipe 缺少必传参数")


    @staticmethod
    def wati_element(el,timeout=3,interval=0.5,intervalfunc=None,rgb=False,threshold=0.85):
        element = Template(el, rgb=rgb, threshold=threshold)
        pos = wait(element,timeout=timeout,interval=interval,intervalfunc=intervalfunc)
        return pos