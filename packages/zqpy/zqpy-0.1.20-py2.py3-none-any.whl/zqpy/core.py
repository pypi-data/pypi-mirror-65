# Insert your code here. 
print(" Init zqpy core By ZhouQing")
from .pkg import *       # 直接可以调用Class, 因为init里面注册了

def vGetLogTag():
    return "BasePyClass"

def vLocallizePath():
    return None

Log = LogServiceClass(tag=vGetLogTag())
LogD = Log.LogD
LogW = Log.LogW
LogE = Log.LogE
FileService = FileServiceClass()
HttpService = HttpServiceClass()
RegexService = RegexServiceClass()
ThreadService = ThreadServiceClass()
TimeService = TimeServiceClass()
VideoDownloadService = VideoDownloadServiceClass()
LocalizeService = LocallizeServiceClass(path=(vLocallizePath() or None))
WaitExecutService = WaitExecutServiceClass()
QrCodeService = QrCodeServiceClass()
ToolsService = ToolsServiceClass()
MailService = MailServiceClass()
########################################通用方法##########################################
def GetLocalize(key):
    return LocalizeService.Get(key)

############################################子类可重写##########################################