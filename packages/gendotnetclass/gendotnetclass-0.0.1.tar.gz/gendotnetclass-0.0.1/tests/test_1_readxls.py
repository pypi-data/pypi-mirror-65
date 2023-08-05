# encoding:UTF-8 
import pytest
from Library.Container import Configs,Xls

class TestXls:
    Configs.config.override({
        "filename": "templates/tableStructure.xlsx",
        "templateDir": "templates",
        "TableName": "FormMaster",
        "tempFileName": "CshapeTemplate.mako"            
    })
    xlsObj = Xls.xls_client()
    
    @pytest.mark.skip(reason="skip this")
    def test_sheetNameGreateThanZero(self):
        print(f"\nsheet數： {len(self.xlsObj.getSheetNames())}") 
        for name in self.xlsObj.getSheetNames():
            print(f"{name}")

        assert len(self.xlsObj.getSheetNames()) > 0

    @pytest.mark.skip(reason="skip this")
    def test_getSheetData(self):
        for name in self.xlsObj.getSheetNames():
            print(f"sheet name:{name}")
            for row in self.xlsObj.getSheetData(name):
                print(row)

    @pytest.mark.skip(reason="skip this")
    def test_getFieldTitle(self):
        print(self.xlsObj.fieldTitle('FormMaster',3))

    @pytest.mark.skip(reason="skip this")
    def test_getRows(self):
        for sheetName in self.xlsObj.getSheetNames(['Index']):
            print(f"sheet name:{sheetName}")
            fieldTitles = self.xlsObj.fieldTitle(sheetName,3)
            for field in self.xlsObj.GetRows(sheetName):
                print(field)

    @pytest.mark.skip(reason="skip this")
    def test_getEnumNotNone(self):
        for sheetName in self.xlsObj.getSheetNames(['Index']):
            print(f"sheet name:{sheetName}")
            fieldTitles = self.xlsObj.fieldTitle(sheetName,3)
            enumDicts = []
            for field in (field for field in self.xlsObj.GetRows(sheetName) if field.enum != None):
                print(f"{field.fieldName}")
                enumlist = field.enum.split()
                enumDict = {}
                for item in enumlist:
                    itemdetail = item.split('.')
                    print(f"{itemdetail[0]}-{itemdetail[1]}")
                    enumDict.update({itemdetail[1]:itemdetail[0]})
                enumDicts.append({'fieldName':field.fieldName,'enumDict':enumDict})
            
            print(enumDicts)
            #     enumDict = {}
            #     for item in field.enum:
            #         enum = item.split('.')
            #         enumDict.update( {enum[1] : enum[0]} )
            #     enumDicts.append(enumDict)
            # print(enumDicts)

    @pytest.mark.skip(reason="skip this")
    def test_getFkTableNotNone(self):
        fkTables = []
        for sheetName in self.xlsObj.getSheetNames(['Index']):
            print(f"sheet name:{sheetName}")
            fieldTitles = self.xlsObj.fieldTitle(sheetName,3)
            for field in (field for field in self.xlsObj.GetRows(sheetName) if field.fkTable != None):
                fkTables.append({"master":field.fkTable,"slave":sheetName})

        print(fkTables)
