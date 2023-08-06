from contextlib import closing
import requests
import os
from LogService import LogServiceClass

class VideoDownloadServiceClass(object):
    Log = LogServiceClass(tag="VideoDownloadServiceClass")
    LogD = Log.LogD
    LogW = Log.LogW
    LogE = Log.LogE
    def __init__(self, *args):
        pass
    
    def Down(self, urlPath, saveFilePath, isCoverFile = False):
        try:
            if isCoverFile and os.path.exists(saveFilePath):
                os.remove(saveFilePath)
            with closing(requests.get(urlPath, stream=True)) as response:
                if not response.ok:
                    print('错误页面：==>>>  ' + response.text)
                    return False, saveFilePath
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if(os.path.exists(saveFilePath) and os.path.getsize(saveFilePath)==content_size):
                    print('跳过'+saveFilePath)
                    return False, saveFilePath
                else:
                    if not ".mp4" in saveFilePath.lower():
                        saveFilePath = saveFilePath + ".mp4" 
                    videoDirPath = os.path.dirname(saveFilePath)
                    if not os.path.exists(videoDirPath):
                        os.makedirs(videoDirPath)
                    progress = ProgressBar(saveFilePath, total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载",fin_status="下载完成")
                    with open(saveFilePath, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            progress.refresh(count=len(data))
            return True, saveFilePath
        except BaseException as e:
            self.LogE("Down error ==>>  " + str(e))
            return False, saveFilePath

#下载进度
class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (
            self.title, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
            self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

if __name__ == "__main__":
    VideoDownloadService = VideoDownloadServiceClass()
    videoUrl = "http://vfx.mtime.cn/Video/2019/03/21/mp4/190321153853126488.mp4"
    VideoDownloadService.Down(videoUrl, "Video/测试.mp4")