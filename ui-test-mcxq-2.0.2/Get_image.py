

class Get_image():
    #初始化图片文件路劲
    def __init__(self,road):
        self.road = road

    def img_name(self, imag_name,rgb=False):
        #输入名称获取图片完整地址
        if rgb == False:
            img = r"/Users/panshuhuai/PycharmProjects/ui-test-mcxq-2.0.2/%s/%s.png"%(self.road,imag_name)
        else:
            img = r"/Users/panshuhuai/PycharmProjects/ui-test-mcxq-2.0.2/%s/%s.png" % (self.road, imag_name)
        return img
