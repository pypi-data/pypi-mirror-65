from mako.template import Template
from mako.lookup import TemplateLookup

class GenControllers:
    def __init__(self,config):
        """設定template的目錄"""
        self.config = config
        templateDir = self.config.get('templateDir')
        self.controllersDir = self.config.get('controllersDir')
        self.tableName = ""
        self.fileName = ""
        self.myLookUp = TemplateLookup(directories=[templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.content = ""
        
    def RenderControllers(self,data=[]):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('tempControllersFileName')
        mytemplate = self.myLookUp.get_template(tempFileName)
        self.content = mytemplate.render(TableName = self.tableName,mapRows=data)

    def GenControllersFile(self,tableName,maprows):
        self.tableName = tableName
        self.fileName = f"{self.controllersDir}/{self.tableName}Controller.cs"
        self.RenderControllers(maprows)