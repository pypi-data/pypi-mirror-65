from mako.template import Template
from mako.lookup import TemplateLookup

class GenInterface:
    def __init__(self,config):
        """設定template的目錄"""
        self.config = config
        templateDir = self.config.get('templateDir')
        self.interfaceDir = self.config.get('interfaceDir')
        self.tableName = ""
        self.fileName = ""
        self.myLookUp = TemplateLookup(directories=[templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.content = ""
        
    def RenderInterface(self):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('tempInterfaceFileName')
        mytemplate = self.myLookUp.get_template(tempFileName)
        self.content = mytemplate.render(TableName = self.tableName)

    def GenInterfaceFile(self,tableName):
        self.tableName = tableName
        self.fileName = f"{self.interfaceDir}/I{self.tableName}Repository.cs"
        self.RenderInterface()