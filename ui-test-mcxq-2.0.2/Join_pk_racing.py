import requests
import jsonpath
import time
import sys


class test_join():
    def Check_User_token(self,mobileNo):
        mobilestr = str(mobileNo)
        print("测试用户： %s 开始加入测试环境比赛" % (mobilestr))
        url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
        data = {
            "mobileNo": mobileNo
        }
        headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                   "cookie": "JSESSIONID=D433BE61468E97C1%s31C6DE322B0A8D2" }
        for z in range(5):
            time.sleep(5)
            try:
                resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                if jsonpath.jsonpath(resp.json(), '$.status')[0] ==200 :
                    self.Check_User_token(mobileNo)
                    sys.exit()  # 重新启动程序，完成后退出
                elif jsonpath.jsonpath(resp.json(), '$.status')[0] == 0:
                    break
            except:
                print("/generateOTP timeout")
        print(resp.json())
        resp.json()
        signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]
        resp.close()

        url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
        headers = {'Content-Type': 'application/json'}
        data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
        for z in range(3):
            try:
                resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                if resp.status_code == 200:
                    print("validate/login: %s" % (resp.json()))
                    break
            except:
                print("/login timeout")
        cid = jsonpath.jsonpath(resp.json(), "$.data.cid")[0]  # 获取cid
        token = jsonpath.jsonpath(resp.json(), "$.data.token")[0]  # 获取token
        print("cid: %s"%(cid))
        print("token: %s"%(token))
        resp.close()




    def Query_user_pk(self, mobileNo):
        self.mobileNo = mobileNo
        # 查询用户PK查询
        url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
        data = {
            "mobileNo": self.mobileNo
        }
        headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                   "cookie": "JSESSIONID=D433BE61468E97C1131C6DE322B0A8D2"}
        for z in range(3):
            try:
                resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                if resp.status_code == 200:
                    break
            except:
                print("/generateOTP timeout")
        resp.json()
        signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]
        resp.close()

        url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
        headers = {'Content-Type': 'application/json'}
        data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
        resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
        print(resp.json())
        token = jsonpath.jsonpath(resp.json(), "$.data.token")[0]  # 获取token
        resp.close()
        print(token)

        url = "https://qa-api.ipetapi.com/ipet/user/pk/history"  # 用户战绩查询
        headers = {'Content-Type': 'application/json', "Authorization": token}
        data = {"pageNo": 1, "pageSize": 20, "cupStatus": 1}
        for z in range(3):
            try:
                resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                if resp.status_code == 200:
                    break
            except:
                print("/history timeout")
        print(resp.json())
        for x in range(20):
            user_cupNo = jsonpath.jsonpath(resp.json(), "$.data[%s].cupNo" % (x))[0]
            user_pk_status = jsonpath.jsonpath(resp.json(), "$.data[%s].status" % (x))[0]
            if user_pk_status == 1:
                print(user_cupNo)
                resp.close()
                return user_cupNo
            else:
                pass

    def Uesr_jion_pk(slef, cupNo, number=400, mobileNo=1):
        # 循环参加指定比赛接口
        test_phone_number = 13916280000
        slef.cupNo = cupNo
        for i in range(number):
            time.sleep(3)
            w = mobileNo + i
            test_mobile = test_phone_number + (w)  # 跑到61
            mobilestr = str(test_mobile)
            print("测试用户： %s 开始加入测试环境比赛" % (mobilestr))
            url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
            data = {
                "mobileNo": mobileNo
            }
            headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                       "cookie": "JSESSIONID=D433BE61468E97C1%s31C6DE322B0A8D2" % (i)}
            for z in range(5):
                time.sleep(5)
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                    if jsonpath.jsonpath(resp.json(), '$.status')[0] ==200 :
                        slef.Uesr_jion_pk(cupNo=cupNo, number=400, mobileNo=w)
                        sys.exit()  # 重新启动程序，完成后退出
                    elif jsonpath.jsonpath(resp.json(), '$.status')[0] == 0:
                        break
                except:
                    print("/generateOTP timeout")
            print("错误：%s" % jsonpath.jsonpath(resp.json(), '$.status')[0])
            print(resp.json())
            resp.json()
            signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]
            resp.close()

            url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
            headers = {'Content-Type': 'application/json'}
            data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                    "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                    "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                    "phoneNo": test_mobile, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
            for z in range(3):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                    if resp.status_code == 200:
                        print("validate/login: %s" % (resp.json()))
                        break
                except:
                    print("/login timeout")
            cid = jsonpath.jsonpath(resp.json(), "$.data.cid")[0]  # 获取cid
            token = jsonpath.jsonpath(resp.json(), "$.data.token")[0]  # 获取token
            resp.close()
            print(token)
            time.sleep(1)

            url = 'https://qa-api.ipetapi.com/ipet/user/album'  # 用户相册查询
            headers = {"Content-Type": "application/json", "Authorization": token}
            data = {"pageNo": 1, "pageSize": 10}
            for z in range(3):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                    print("/user/album :%s" % (resp.json()))
                    if resp.status_code == 200:
                        break
                except:
                    print("/album timeout")
            workNo = jsonpath.jsonpath(resp.json(), "$.data[0].workNo")[0]  # 获取已上传素材
            print("workNo: %s" % (workNo))
            resp.close()

            url = "https://qa-api.ipetapi.com/ipet/cup/takePart"  # 调用参加锦标赛赛接口
            headers = {"Content-Type": "application/json", "Authorization": token, "Content-Length": "135",
                       "Accept": "application/json"}
            data = {"cupNo": str(slef.cupNo), "workNo": workNo, "cid": cid, "costSalmonAmount": 1}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                    if resp.status_code == 200:
                        break
                except:
                    print("/takePart timeout")
            print("/cup/takePart :%s" % (resp.json()))
            resp.close()
            if i == number:
                return True

    def found_user_add_img(self):
        # 用户注册+设置头像+投票（更新DB余额）+上传作品
        e = 0
        for i in range(200):
            mobileNo = 13916280001 + (i)  # 默认值：13916280131 之前是图片
            mobilestr = str(mobileNo)
            print("%s 号码，用户开始注册流程" % (mobileNo))
            url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
            data = {
                "mobileNo": mobileNo
            }
            headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                       "cookie": "JSESSIONID=D433BE61468E97C1131C6DE322B0A8D2"}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    # resp = session.post(json=data, headers=headers, url=url, timeout=(50, 60)).content.decode()
                    if resp.status_code == 200:
                        break
                except:
                    print("/generateOTP timeout")
            resp.json()
            signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]
            resp.close()

            time.sleep(2)
            url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
            headers = {'Content-Type': 'application/json'}
            data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                    "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                    "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                    "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp.status_code == 200:
                        break
                except:
                    print("/alidate/login timeout")
            print(resp.json())
            token = jsonpath.jsonpath(resp.json(), "$.data.token")[0]  # 获取token
            print(token)
            resp.close()

            time.sleep(2)
            url = "https://qa-api.ipetapi.com/ipet/user/modifyOrAddPet"  # 调用用户头像昵称上传接口
            headers = {'Content-Type': 'application/json', "Authorization": token}
            # img2 = "https://qa-vod.ipetapi.com/attachment/C467723B-11D3-407C-A2D7-632F18F11B71.mp4"
            img2 = "https://qa-vod.ipetapi.com/attachment/aa9950f3b7e24ee79a52193563a4b311.jpg"
            data = {"headImg": img2, "nickName": "pan%spanpan" % (mobilestr[-3:])}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60))
                    time.sleep(1)
                    if resp.status_code == 200:
                        break
                except:
                    print("/user/modifyOrAddPet timeout")
            print('%s用户:%s 完成头像上传' % (resp.json(), mobileNo[-3:]))
            e += 1

            time.sleep(2)
            url = 'https://qa-api.ipetapi.com/ipet/pk/recommend'  # 查询推荐接口
            headers = {'Content-Type': 'application/json', "Authorization": token}
            for z in range(5):
                try:
                    resp = requests.get(url=url, headers=headers, timeout=(50, 60))
                    time.sleep(1)
                    if resp.status_code == 200:
                        break
                except:
                    print("/pk/recommend timeout")

            reviewId = jsonpath.jsonpath(resp.json(), "$.data.pkReviewList[0].reviewId")[0]
            workNo = jsonpath.jsonpath(resp.json(), "$.data.pkReviewList[0].competitors[0].workNo")[0]
            voteBy = jsonpath.jsonpath(resp.json(), "$.data.pkReviewList[0].competitors[0].cid")[0]
            resp.close()

            time.sleep(2)
            url = "https://qa-api.ipetapi.com/ipet/pk/vote"  # 投票接口
            headers = {'Content-Type': 'application/json', "Authorization": token}
            data = {"reviewId": reviewId, "workNo": workNo, "voteBy": voteBy}
            for z in range(5):
                try:
                    resp = requests.post(url=url, headers=headers, json=data, timeout=(50, 60))
                    time.sleep(1)
                    if resp.status_code == 200:
                        break
                except:
                    print("ipet/pk/vote timeout")
            print('%s用户:%s 完成投票' % (resp.json(), mobileNo))
            resp.close()

            url = "https://qa-api.ipetapi.com/ipet/user/submit/work"  # 调用用户数据上传接口
            headers = {'Content-Type': 'application/json', "Authorization": token}

            img = "https://qa-vod.ipetapi.com/attachment/C467723B-11D3-407C-A2D7-632F18F11B71.mp4"
            slogans = ["投本旺一票，生活旺旺旺", "咧嘴对你笑,跪求一票", "点我点我点我，生活旺旺旺", "必胜必胜必胜",
                       "快投本喵一票", "16621010586\n"]
            data = {"mediaUrl": img, "desc": "pan", "tags": [r"谁更可爱"], "slogans": slogans, }

            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), verify=False)
                    time.sleep(1)
                    if resp.status_code == 200:
                        break
                except:
                    print("ipet/pk/vote timeout")
            print("%s,%s用户参赛作品上传完成" % (resp.json(), mobileNo))
            resp.close()

    def found_user_pk_vote(self,add_nember=1,Victory_status=0):
        # Victory_status = 0 列表上方用户获胜（日常赛胜利），1-列表下方用户胜利（日常赛失败）
        # 用户登录+投票
        for i in range(300):
            mobileNo = 13916280000 + int(add_nember) + (i)  # 默认值：13916280131 之前是图片
            print("%s 号码，用户开始登录，并进入投票流程" % (mobileNo))
            url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
            data = {
                "mobileNo": mobileNo
            }
            headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                       "cookie": "JSESSIONID=D433BE61468E97C1131C6DE322B0A8D2"}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp.status_code == 200:
                        break
                except:
                    print("/generateOTP timeout")
            signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]  # 调取OTP接口，发送验证码

            # 用户使用白名单进行，OTP登录
            url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
            headers = {'Content-Type': 'application/json'}
            data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                    "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                    "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                    "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
            for x in range(5):
                try:
                    resp_login = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp_login.status_code == 200:
                        break
                except:
                    print("/alidate/login timeout")
            print(resp_login.json())
            token = jsonpath.jsonpath(resp_login.json(), "$.data.token")[0]  # 获取token
            print(token)
            # 获取用户token，通过token调用推荐接口
            url2 = 'https://qa-api.ipetapi.com/ipet/pk/recommend'  # 查询推荐接口
            headers = {'Content-Type': 'application/json', "Authorization": token}
            for v in range(3):  # 每个用户投票多少组
                for r in range(3):
                    try:
                        resp_recommend = requests.get(url=url2, headers=headers, timeout=(50, 60))

                        if jsonpath.jsonpath(resp_recommend.json(), '$.status') == 0:
                            break
                    except:
                        print("/pk/recommend timeout")
                print("用户推荐投票%s" % (resp_recommend.json()))  # 获取到用户登比赛推荐内容
                pkReviewList = jsonpath.jsonpath(resp_recommend.json(), "$.data.pkReviewList")
                # 循环进入
                for p in range(10):  # 一轮中的投票次数
                    number = int(p)
                    pkReviewdLst1 = pkReviewList[0]
                    pkReviewdDict = pkReviewdLst1[number]
                    pkReviewdDict_competitors = pkReviewdDict['competitors']
                    competitors = pkReviewdDict_competitors[int(Victory_status)]  # 筛选一个组中的参数（0为PK首个用户，1为被PK的用户）
                    reviewId = pkReviewdDict['reviewId']

                    workNo = competitors['workNo']
                    voteBy = competitors['cid']
                    # 获取点击投票中的必要参数

                    # 调用投票接口，并带入获取的参数
                    url = "https://qa-api.ipetapi.com/ipet/pk/vote"  # 投票接口
                    headers = {'Content-Type': 'application/json', "Authorization": token}
                    data = {"reviewId": reviewId, "workNo": workNo, "voteBy": voteBy}
                    for z in range(5):
                        try:
                            resp2 = requests.post(url=url, headers=headers, json=data, timeout=(50, 60))
                            time.sleep(1)
                            if resp2.status_code == 200:
                                print("用户:%s 进行投票完成：%s 次" % (mobileNo, p + 1))
                                break
                            if resp2.status_code != 200:
                                print(resp2.json())
                        except:
                            print("ipet/pk/vote timeout")
                    if p == 9:
                        break

    def found_user_pk_vote_and_task(self,add_nember=1,Victory_status=0,gift_id=8):
        # 指定类型投票
        # Victory_status = 0 列表上方用户获胜（日常赛胜利），1-列表下方用户胜利（日常赛失败）
        # gift_id 根据cms配置选择不同的礼物
        # 用户登录+投票+打赏
        for i in range(300):
            mobileNo = 13916280000 +(int(add_nember))+ (i)  # 默认值：13916280131 之前是图片
            print("%s 号码，用户开始登录，并进入投票流程" % (mobileNo))
            url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
            data = {
                "mobileNo": mobileNo
            }
            headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                       "cookie": "JSESSIONID=D433BE61468E97C1131C6DE322B0A8D2"}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp.status_code == 200:
                        break
                except:
                    print("/generateOTP timeout")
            signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]  # 调取OTP接口，发送验证码

            # 用户使用白名单进行，OTP登录
            url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
            headers = {'Content-Type': 'application/json'}
            data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                    "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                    "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                    "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
            for x in range(5):
                try:
                    resp_login = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp_login.status_code == 200:
                        break
                except:
                    print("/alidate/login timeout")
            #print(resp_login.json())
            token = jsonpath.jsonpath(resp_login.json(), "$.data.token")[0]  # 获取token
            user_cid = jsonpath.jsonpath(resp_login.json(), "$.data.cid")[0] #获取登录用户的CID
            print("登录用户cid：%s ,登录用户token: %s"%(user_cid,token))
            # 获取用户token，通过token调用推荐接口
            url2 = 'https://qa-api.ipetapi.com/ipet/pk/recommend'  # 查询推荐接口
            headers = {'Content-Type': 'application/json', "Authorization": token}
            for v in range(3):  # 每个用户投票多少组
                for r in range(3):
                    try:
                        resp_recommend = requests.get(url=url2, headers=headers, timeout=(50, 60))

                        if jsonpath.jsonpath(resp_recommend.json(), '$.status') == 0:
                            break
                    except:
                        print("/pk/recommend timeout")
                print("用户推荐投票%s" % (resp_recommend.json()))  # 获取到用户登比赛推荐内容
                pkReviewList = jsonpath.jsonpath(resp_recommend.json(), "$.data.pkReviewList")
                #获取送礼必须参数
                day_task_dick = {}  # 创建day_task_dick,将/gift/give data中的参数均保存其中。
                for i in range(9):#循环遍历需要的内容
                    # day_task_dick["cid%s"%i] = jsonpath.jsonpath(resp_login.json(), "$.data.pkNo")[i]
                    i = int(i)
                    #print("测试%s"%resp_recommend.json())
                    pk_review_list = jsonpath.jsonpath(resp_recommend.json(), "$.data.pkReviewList")[0]
                    #print("pk_review_list:%s"%pk_review_list)
                    pk_review_dict=pk_review_list[i]
                    #print(pk_review_dict)
                    day_task_dick['pkNo%s' % i] = pk_review_dict['pkNo']
                    competitors_list = pk_review_dict['competitors']
                    competitors_dict = competitors_list[0]
                    day_task_dick['cid%s' % i] = competitors_dict['cid']
                    day_task_dick['workNo%s' % i] = competitors_dict['workNo']


                # 循环进入
                for p in range(10):  # 一轮中的投票次数
                    number = int(p)
                    pkReviewdLst1 = pkReviewList[0]
                    pkReviewdDict = pkReviewdLst1[number]
                    pkReviewdDict_competitors = pkReviewdDict['competitors']
                    competitors = pkReviewdDict_competitors[int(Victory_status)]  # 控制投票
                    reviewId = pkReviewdDict['reviewId']

                    workNo = competitors['workNo']
                    voteBy = competitors['cid']
                    # 获取点击投票中的必要参数

                    # 调用投票接口，并带入获取的参数
                    url = "https://qa-api.ipetapi.com/ipet/pk/vote"  # 投票接口
                    headers = {'Content-Type': 'application/json', "Authorization": token}
                    data = {"reviewId": reviewId, "workNo": workNo, "voteBy": voteBy}
                    for z in range(3):
                        try:
                            resp2 = requests.post(url=url, headers=headers, json=data, timeout=(50, 60))
                            time.sleep(1)
                            if resp2.status_code == 200:
                                print("用户:%s 进行投票完成：%s 次" % (mobileNo, p + 1))
                                break
                            if resp2.status_code != 200:
                                print(resp2.json())
                        except:
                            print("ipet/pk/vote timeout")
                    if p == 9:
                        for f in range(10):#打赏次数
                           url = 'https://qa-api.ipetapi.com/ipet/gift/give'
                           headers_task = {'Content-Type': 'application/json', "Authorization": token}
                           data = {"cid":day_task_dick['cid%s'%f],"workNo":day_task_dick['workNo%s'%f],"pkNo":day_task_dick['pkNo%s'%f],'giftIdList':[int(gift_id)]}
                           for i in range(3):#请求循环
                               try:
                                   resp_task = requests.post(url=url, headers=headers_task, json=data, timeout=(50, 60))#调用搭上接口
                                   time.sleep(1)
                                   if resp_task.status_code == 200:
                                       print("用户:%s 打赏：%s 次" % (mobileNo, f + 1))
                                       break
                                   if resp_task.status_code != 200:
                                       print(resp_task.json())
                               except:
                                   print("ipet/gift/give timeout")

    def User_jion_Dpk(self,add_nember):
        #用户自动加入日常赛方法  （isWinner：判断是否结束，结束为true，returnType：2进行中，1未开始）
        for i in range(300):
            mobileNo = 13916280000 +(int(add_nember))+ (i)  # 默认值：13916280131 之前是图片
            print("%s 号码，用户开始登录，并进入投票流程" % (mobileNo))
            url = "https://qa-api.ipetapi.com/ipet/validate/generateOTP"  # 发送短信验证码接口调用
            data = {
                "mobileNo": mobileNo
            }
            headers = {"Content-Type": "application/json", "device-name": "apple", "os": "ios",
                       "cookie": "JSESSIONID=D433BE61468E97C1131C6DE322B0A8D2"}
            for z in range(5):
                try:
                    resp = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp.status_code == 200:
                        break
                except:
                    print("/generateOTP timeout")
            signFactor = jsonpath.jsonpath(resp.json(), '$.data.signFactor')[0]  # 调取OTP接口，发送验证码

            # 用户使用白名单进行，OTP登录
            url = "https://qa-api.ipetapi.com/ipet/validate/login"  # 用户登录注册接口（返回cid,token）
            headers = {'Content-Type': 'application/json'}
            data = {"signFactor": signFactor, "verifyCode": "", "appPushId": "", "loginType": 2,
                    "ipAddress": "192.168.22.85", "operateType": "", "bundleId": "", "otp": "123456",
                    "deviceId": "8F46F257-5AC4-4113-B41A-6791F22F76FC-1701768500.550853", "deviceName": "",
                    "phoneNo": mobileNo, "deviceInfo": "", "gwAuth": "", "loginPlat": "1", "jtSafeKey": ""}
            for x in range(5):
                try:
                    resp_login = requests.post(json=data, headers=headers, url=url, timeout=(50, 60), proxies={})
                    if resp_login.status_code == 200:
                        break
                except:
                    print("/alidate/login timeout")
            #print(resp_login.json())
            token = jsonpath.jsonpath(resp_login.json(), "$.data.token")[0]  # 获取token
            user_cid = jsonpath.jsonpath(resp_login.json(), "$.data.cid")[0] #获取登录用户的CID
            print("登录用户cid：%s ,登录用户token: %s"%(user_cid,token))
            dpk_url = 'https://qa-api.ipetapi.com/ipet/validate/login' #查询或发起日常赛详情信息
            dpk_data = {"cid":user_cid,"isTakePart":True}
            for z in range(3):
                try:
                    dpk_resp = requests.post(json=dpk_data,headers=headers,url=dpk_url,timeout=(50,60))
                    if dpk_resp.status_code == 200:
                        break
                except:
                    print("/validate/login timeout")



if __name__ == '__main__':
    aa = test_join()
    aa.Check_User_token(16621010586) #获取cid 和 token
    # aa.found_user_add_img() #给白名单用户添加作品和头像
    # cupNo=aa.Query_user_pk(mobileNo='16621010586')  #此号码一定要有未开始的比赛
    # aa.Uesr_jion_pk(cupNo='CUP23071318415951006001',mobileNo=1) #加入比赛接口
    # aa.found_user_pk_vote(add_nember=25,Victory_status=0) #投票接口
    # aa.found_user_pk_vote_and_task(add_nember=10,Victory_status=0,gift_id=14)  #用户投票+完成指定任务并打赏

    # 13916280022 测试手机号
