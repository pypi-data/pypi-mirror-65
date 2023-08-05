class ToolsServiceClass(object):
    def ToNumberCompany(self, number):
        if number > 100000000:
            return number/100000000 + "亿"
        elif number > 10000000:
            return number/10000000 + "千万"
        elif number > 1000000:
            return number/1000000 + "百万"
        elif number > 100000:
            return number/100000 + "十万"
        elif number > 10000:
            return number/10000 + "万"
        else:
            return number
    
    #https://www.runoob.com/markdown/md-block.html
    def SendNotify(self, title="zq_python", desc="", isMerge=True):
        from HttpService import HttpServiceClass
        if len(title + '-->' + desc) < 256 and isMerge:
            title = title + '-->'  + desc
        httpService = HttpServiceClass()
        params = {"text": title, "desp": desc}
        print("方糖发送内容：{}".format(params))
        try:
            urlRequest = httpService.GetUrlResetByRequests("https://sc.ftqq.com/SCU63651T3c16cbd7d3aa23d56645aeddc3459c135d9aebde1ca0a.send", params=params, headers={'Connection':'close'}, verify = False)
            urlRequest.close()
        except BaseException as e:
            print("方糖内容发送出错： ", str(e))
            urlRequest.close()
        finally:
            pass