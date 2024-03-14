import os
import sys

current_dir = os.getcwd()                   # noqa #isort:skip
sys.path.append(current_dir + '/source/')   # noqa #isort:skip

from eralchemy2 import render_er

from source.db.models.buildings import BaseCommon, Building
from source.db.models.persons import Person
from source.db.models.rooms import Room
from source.db.models.vendors import Vendor

print(BaseCommon.metadata.tables)
if __name__ == '__main__':

    render_er(BaseCommon, 'erd.png')
