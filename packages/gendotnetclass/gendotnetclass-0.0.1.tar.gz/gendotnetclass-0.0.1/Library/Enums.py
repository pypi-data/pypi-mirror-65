# -*- coding: utf-8 -*-
from enum import Enum
 
class Command(Enum):
    NEW = 'new'
    ADD = 'add'
    RUN = 'run'
    BUILD = 'build'
    PUBLISH = 'publish'
    STORE = 'store'
    TEST = 'test'

class ProjectKind(Enum):
    CLASSLIB = 'classlib'
    WEBAPI = 'webapi'
    CONSOLE = 'console'
    MVC = 'mvc'
    MSTEST = 'mstest'
    SLN = 'sln'
    REACTREDUX = 'reactredux'

class Package(Enum):
    ADD = 'add'
    LIST = 'list'
    REMOVE = 'remove'