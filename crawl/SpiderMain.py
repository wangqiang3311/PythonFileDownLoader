from  DataOutput import DataOutput
from  FileDownLoader  import FileDownLoader
from  FileParser  import FileParser
from  UrlManager import UrlManager

import os
import time
import random

class SpiderMain(object):
    def __init__(self):
        self.manager=UrlManager()
        self.downloader=FileDownLoader()
        self.parser=FileParser()
        self.output=DataOutput()

    def crawl(self,root_files):

        for root_file in root_files:
            new_urls=self.parser.parser(root_file)
            self.manager.add_new_urls(new_urls)

            while(self.manager.has_new_url()):
                try:
                    new_url=self.manager.get_new_url()
                    data=self.downloader.download(new_url)
                    self.output.store_data(data,root_file,new_url)
                    print("已经抓取%s个链接"%self.manager.old_url_size())

                    interval = random.randint(1, 3)
                    
                    time.sleep(interval)
                    print("sleep: %d" %interval)

                except Exception as err:
                    self.output.mark_result(root_file,new_url,False)
                    print("crawl faild:"+str(err))

if __name__=="__main__":
    spider_main=SpiderMain()
    file_list=[]
    #传入excel文件，下载里面pdf文件
    for root,dirs,files in os.walk("crawl/files"):
        for file in files:
            filepath=os.path.join(root,file)
            file_list.append(filepath)

    spider_main.crawl(file_list)

    
