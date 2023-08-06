import re

class RegexServiceClass(object):

    # 获取URL  返回数组
    def GetRegexUrl(self, content):
        urlRegex = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2})*/)+', content)
        return urlRegex 
    
    # 获取"" 中的内容  返回数组
    def GetRegexDoubleQuotation(self, content):
        pattern = re.compile('"(.*)"')
        resultData = pattern.findall(content)
        return resultData 
    
    # 获取a b 之间的内容  返回数组
    def GetRegexBetweenContent(self, a, b, content):
        result = re.findall(".*%s(.*)%s.*"%(a,b),content)
        '''
        print(result)
        for x in result:
            print(x)
        '''
        return result