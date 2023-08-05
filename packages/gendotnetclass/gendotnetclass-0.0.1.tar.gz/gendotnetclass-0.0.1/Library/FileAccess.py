import os
from os import listdir
from os.path import isfile, isdir, join
from os import path
import yaml

class FileAccess:

    def __init__(self):
        pass

    def checkPath(self,myPath):
        '''若class目錄不存在則建立'''
        if (not path.exists(myPath)):
            os.mkdir(myPath)      

    def DelFile(self,fileName):            
        if os.path.exists(fileName):
            os.remove(fileName)

    def Save(self,fileName,content):
        """設定存檔的檔名"""
        f= open(fileName,"w+")
        f.write(content)
        f.close()

    def showFilesContent(self,filePath):    
        """ 取得所有檔案與子目錄名稱
        以迴圈處理 """
        for f in listdir(filePath):
            # 產生檔案的絕對路徑
            fullpath = join(filePath, f)
            # 判斷 fullpath 是檔案還是目錄
            if isfile(fullpath):
                lines = open(fullpath, "r")
                for line in [line for line in lines if (line != None)]:
                    print(line)
            elif isdir(fullpath):
                print("目錄：", f)          
                        
if __name__ == "__main__":
    readFile = FileAccess()
    readFile.test_showDetail()
