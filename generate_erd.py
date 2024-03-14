import os
import sys

current_dir = os.getcwd()                   # noqa #isort:skip
sys.path.append(current_dir + '/source/')   # noqa #isort:skip

import pip


def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


if __name__ == '__main__':
    install('eralchemy2')
    install('sqlalchemy')
    from db.models.base import BaseCommon
    from eralchemy2 import render_er

    from source.db.models.buildings import Building
    from source.db.models.persons import Person
    from source.db.models.rooms import Room
    from source.db.models.vendors import Vendor
    render_er(BaseCommon, 'erd.png')
