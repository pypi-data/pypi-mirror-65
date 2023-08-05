from mako.template import Template
from mako.lookup import TemplateLookup


class GenCshape:
    def __init__(self,config):
        """設定template的目錄"""
        self.config = config
        templateDir = self.config.get('templateDir')
        self.classDir = self.config.get('classDir')
        self.tableName = ""
        self.fileName = ""
        self.dbContentFileName = ""
        self.myLookUp = TemplateLookup(directories=[templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.content = ""
        self.dbContent = ""
        
    def RenderCS(self,innerTables,data=[]):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('tempFileName')
        mytemplate = self.myLookUp.get_template(tempFileName)
        self.content = mytemplate.render(TableName = self.tableName,mapRows=data,innerTables = innerTables)

    def RenderDBContent(self,data=[]):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('dbTempFileName')
        mytemplate = self.myLookUp.get_template(tempFileName)
        self.dbContent = mytemplate.render(TableNames=data)

    def GenCSFile(self,tableName,maprows,innerTables):
        self.tableName = tableName
        self.fileName = f"{self.classDir}/{self.tableName}.cs"
        self.RenderCS(innerTables,maprows)

    def GenDBContentFile(self,tableNames):
        self.dbContentFileName = f"{self.classDir}/MyDbContent.cs"
        self.RenderDBContent(tableNames)

