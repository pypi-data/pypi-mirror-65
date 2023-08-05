from mako.template import Template
from mako.lookup import TemplateLookup

class GenRepository:
    def __init__(self,config):
        """設定template的目錄"""
        self.config = config
        templateDir = self.config.get('templateDir')
        self.repositoryDir = self.config.get('repositoryDir')
        self.tableName = ""
        self.fileName = ""
        self.myLookUp = TemplateLookup(directories=[templateDir], input_encoding='utf-8', encoding_errors='replace')
        self.content = ""
        
    def RenderRepository(self):
        """設定template的檔案 
           設定寫入版型的變數 
        """
        tempFileName = self.config.get('tempRepositoryFileName')
        mytemplate = self.myLookUp.get_template(tempFileName)
        self.content = mytemplate.render(TableName = self.tableName)

    def GenRepositoryFile(self,tableName):
        self.tableName = tableName
        self.fileName = f"{self.repositoryDir}/{self.tableName}Repository.cs"
        self.RenderRepository()