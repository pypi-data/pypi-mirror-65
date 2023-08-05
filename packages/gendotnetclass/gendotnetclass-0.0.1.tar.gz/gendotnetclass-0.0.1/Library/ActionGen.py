
class ActionGen:
    """組合各元件執行商務邏輯"""
    def __init__(self,Xls,Gen,GenEnum,GenControllers,GenInterface,GenRepository,FileAccess):
        """設定template的目錄"""
        self.Xls=Xls
        self.Gen=Gen
        self.GenEnum=GenEnum
        self.GenControllers=GenControllers
        self.GenInterface=GenInterface
        self.GenRepository=GenRepository
        self.File = FileAccess

    def genGenericInterface(self):
        generic = """ 
using System.Linq;
using System.Threading.Tasks;
namespace DataAccess.Interfaces
{
    public interface IGenericRepository<TEntity>
        where TEntity : class
    {
        IQueryable<TEntity> GetAll();
        Task<TEntity> GetById(int id);
        Task Create(TEntity entity);
        Task Update(int id, TEntity entity);
        Task Delete(int id);
    }
}
    """    
        self.File.checkPath(self.GenInterface.interfaceDir)    
        self.File.Save('Interfaces/IGenericRepository.cs',generic)      

    def genericRepository(self):
        repo = """
using System;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    public class GenericRepository<TEntity> : IGenericRepository<TEntity>
        where TEntity : class
    {
        private readonly MyDBContext _dbContext;

        public GenericRepository(MyDBContext dbContext)
        {
            _dbContext = dbContext;
        }

        public IQueryable<TEntity> GetAll()
        {
            return _dbContext.Set<TEntity>().AsNoTracking();
        }

        public async Task<TEntity> GetById(int id)
        {
            return await _dbContext.Set<TEntity>().FindAsync(id);
        }

        public async Task Create(TEntity entity)
        {
            await _dbContext.Set<TEntity>().AddAsync(entity);
            await _dbContext.SaveChangesAsync();
        }

        public async Task Update(int id, TEntity entity)
        {
            _dbContext.Set<TEntity>().Update(entity);
            await _dbContext.SaveChangesAsync();
        }

        public async Task Delete(int id)
        {
            var entity = await _dbContext.Set<TEntity>().FindAsync(id);
            _dbContext.Set<TEntity>().Remove(entity);
            await _dbContext.SaveChangesAsync();
        }
    }
}
        """  
        self.File.checkPath(self.GenRepository.repositoryDir)    
        self.File.Save('Repository/GenericRepository.cs',repo)      

    def genClass(self):
        """執行產生Code First Class"""
        self.File.checkPath(self.Gen.classDir)    
        sheetNames = self.Xls.getSheetNames()
        fkTables = self.Xls.GetFkTableNotNone()
        # 產生DBContent
        self.Gen.GenDBContentFile(sheetNames)   
        self.File.Save(self.Gen.dbContentFileName,self.Gen.dbContent)      

        for sheetName in sheetNames:
            rows = self.Xls.GetRows(sheetName)
            innerTables = [fkTable for fkTable in fkTables if fkTable['master'] == sheetName]

            # 產生Model Class
            self.Gen.GenCSFile(sheetName,rows,innerTables)   
            self.File.Save(self.Gen.fileName,self.Gen.content)      
            # 產生Enum
            self.GenEnum.GenEnumCSFile(rows)
            self.File.Save(self.GenEnum.fileName,self.GenEnum.content)   
        #  查看產生的DotNetClass
        # self.File.showFilesContent(self.Gen.classDir)
  
    def genControllers(self):
        """執行產生Asp.net Core Controllers"""
        self.File.checkPath(self.GenControllers.controllersDir)    
        sheetNames = self.Xls.getSheetNames()
        for sheetName in sheetNames:
            rows = self.Xls.GetRows(sheetName)
            # 產生Asp.net Core Controllers
            self.GenControllers.GenControllersFile(sheetName,rows)   
            self.File.Save(self.GenControllers.fileName,self.GenControllers.content)      

    def genInterface(self):
        """執行產生Asp.net Core Interface"""
        self.File.checkPath(self.GenInterface.interfaceDir)    
        sheetNames = self.Xls.getSheetNames()
        for sheetName in sheetNames:
            # 產生Asp.net Core Interface
            self.GenInterface.GenInterfaceFile(sheetName)   
            self.File.Save(self.GenInterface.fileName,self.GenInterface.content)      

    def genRepository(self):
        """執行產生Asp.net Core Repository"""
        self.File.checkPath(self.GenRepository.repositoryDir)    
        sheetNames = self.Xls.getSheetNames()
        for sheetName in sheetNames:
            # 產生Asp.net Core Repository
            self.GenRepository.GenRepositoryFile(sheetName)   
            self.File.Save(self.GenRepository.fileName,self.GenRepository.content)      
        
