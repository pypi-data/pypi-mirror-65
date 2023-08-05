from mako.template import Template
from mako.lookup import TemplateLookup
import os
import os.path
from os import path


class GenEnumCs:
    def __init__(self,config):
        """設定template的目錄"""
        self.config = config
        self.templateDir = self.config.get('templateDir')
        self.classDir = self.config.get('classDir')
        self.mylookup = TemplateLookup(directories=[self.templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.fileName = f"{self.classDir}/EnumList.cs"
        self.enumDicts = []
        self.content = ""
        
    def RenderEnumCS(self):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('tempEnumFileName')
        mytemplate = self.mylookup.get_template(tempFileName)
        self.content = mytemplate.render(enumDicts = self.enumDicts)

    def GenEnumCSFile(self,maprows):
        # 產生Enum
        # 取得enum直欄不等於None
        for field in (field for field in maprows if field.enum):
            # print(f"{field.fieldName}")
            enumlist = field.enum.split()
            enumDict = {}
            for item in enumlist:
                itemdetail = item.split('.')
                # print(f"{itemdetail[0]}-{itemdetail[1]}")
                enumDict.update({itemdetail[1]:itemdetail[0]})
            self.enumDicts.append({'fieldName':field.fieldName,'enumDict':enumDict})
        self.RenderEnumCS()
