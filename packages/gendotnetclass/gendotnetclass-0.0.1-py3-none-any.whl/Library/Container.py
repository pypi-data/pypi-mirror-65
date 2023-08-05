from dependency_injector import providers, containers
from Library.ReadXls import ReadXls
from Library.GenCshape import GenCshape
from Library.GenControllers import GenControllers 
from Library.GenEnumCs import GenEnumCs
from Library.ActionGen import ActionGen
from Library.FileAccess import FileAccess
from Library.GenInterface import GenInterface
from Library.GenRepository import GenRepository

class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    
class Xls(containers.DeclarativeContainer):
    xls_client = providers.Singleton(ReadXls, Configs.config)

class GenClass(containers.DeclarativeContainer):
    gen_client = providers.Singleton(GenCshape, Configs.config)

class GenControllers(containers.DeclarativeContainer):
    gencontrollers_client = providers.Singleton(GenControllers, Configs.config)

class GenEnum(containers.DeclarativeContainer):
    genenum_client = providers.Singleton(GenEnumCs, Configs.config)

class GenInterface(containers.DeclarativeContainer):
    geninterface_client = providers.Singleton(GenInterface, Configs.config)

class GenRepository(containers.DeclarativeContainer):
    genrepository_client = providers.Singleton(GenRepository, Configs.config)

class FileAccess(containers.DeclarativeContainer):
    file_client = providers.Singleton(FileAccess)

class Action(containers.DeclarativeContainer):
    action = providers.Factory(ActionGen,Xls=Xls.xls_client,Gen=GenClass.gen_client,GenControllers=GenControllers.gencontrollers_client,GenEnum = GenEnum.genenum_client,GenInterface = GenInterface.geninterface_client,GenRepository = GenRepository.genrepository_client ,FileAccess=FileAccess.file_client)
